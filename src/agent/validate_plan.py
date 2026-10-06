"""Member 2 - Plan validation against the real data schema (Contract A).

validate_plan() never raises. It returns either the same plan (all checks passed)
or a CannotDeterminePlan / ClarificationPlan explaining why not.

Contract A is used as-is. One OPTIONAL per-table field is used if Member 1 provides it:
  "years": [2023, 2024]   -> distinct years found in the date column
If "years" is absent, year checks are skipped.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from .plan_schema import (
    AnswerablePlan, CannotDeterminePlan, ClarificationPlan, Plan,
)

NUMERIC_TYPES = {"int", "float"}
ORDERED_TYPES = NUMERIC_TYPES | {"datetime"}   # allowed for min/max


def _cant(reason: str) -> CannotDeterminePlan:
    return CannotDeterminePlan(status="cannot_determine", reason=reason)


def _find_table(schema: Dict[str, Any], name: str) -> Optional[Dict[str, Any]]:
    for t in schema.get("tables", []):
        if t.get("name") == name:
            return t
    return None


def validate_plan(plan: Plan, schema: Dict[str, Any]) -> Plan:
    # Refusals / clarifications pass through untouched.
    if not isinstance(plan, AnswerablePlan):
        return plan

    table = _find_table(schema, plan.table)
    if table is None:
        names = [t.get("name") for t in schema.get("tables", [])]
        return _cant(f"Table '{plan.table}' does not exist. Available tables: {names}.")
    cols: Dict[str, str] = table.get("columns", {})

    def need(col: Optional[str], what: str, tname: str = plan.table, tcols=cols):
        if col is not None and col not in tcols:
            return _cant(f"Column '{col}' ({what}) does not exist in table '{tname}'. "
                         f"Available columns: {list(tcols)}.")
        return None

    # --- existence checks -------------------------------------------------
    for col, what in [(plan.column, "value column"), (plan.group_by, "group_by")]:
        err = need(col, what)
        if err:
            return err
    for fcol in plan.filters:
        err = need(fcol, "filter")
        if err:
            return err

    # --- type checks ------------------------------------------------------
    op = plan.operation.replace("group_", "")
    if plan.column is not None:
        ctype = cols[plan.column]
        if op in ("sum", "average") and ctype not in NUMERIC_TYPES:
            return _cant(f"Cannot compute {op} of '{plan.column}': its type is '{ctype}', not numeric.")
        if op in ("min", "max") and ctype not in ORDERED_TYPES:
            return _cant(f"Cannot compute {op} of '{plan.column}': its type is '{ctype}'.")

    # --- date filter ------------------------------------------------------
    df = plan.date_filter
    if df is not None:
        err = need(df.column, "date_filter")
        if err:
            return err
        if cols[df.column] != "datetime":
            return _cant(f"Column '{df.column}' is '{cols[df.column]}', not a date column.")
        years = table.get("years")
        if years:
            if df.year is not None and df.year not in years:
                return _cant(f"No records exist for year {df.year}. "
                             f"Years available in '{plan.table}': {sorted(years)}.")
            if df.month is not None and df.year is None and len(years) > 1:
                return ClarificationPlan(
                    status="clarification_required",
                    reason=f"Month {df.month} appears in multiple years: {sorted(years)}.",
                    question="Which year do you mean?",
                )

    # --- join -------------------------------------------------------------
    if plan.join is not None:
        right = _find_table(schema, plan.join.table)
        if right is None:
            return _cant(f"Join table '{plan.join.table}' does not exist.")
        err = need(plan.join.left_on, "join key", plan.table, cols)
        if err:
            return err
        err = need(plan.join.right_on, "join key", right["name"], right.get("columns", {}))
        if err:
            return err

    return plan