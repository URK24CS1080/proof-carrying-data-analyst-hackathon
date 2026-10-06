from .executor import execute_plan
from .proof_generator import generate_proof
from ..verifier.verifier import verify_proof


def _build_evidence(
    plan: dict,
    execution_result: dict,
) -> dict:
    """
    Build human-readable evidence from the analysis plan
    and execution result.
    """

    table = plan.get("table")
    column = plan.get("column")
    group_by = plan.get("group_by")
    filters = plan.get("filters") or {}
    date_filter = plan.get("date_filter")
    join_config = plan.get("join")
    operation = plan.get("operation")

    # ---------------------------------------------
    # TABLES USED
    # ---------------------------------------------

    tables_used = []

    if table:
        tables_used.append(table)

    if isinstance(join_config, dict):
        join_table = join_config.get("table")

        if join_table and join_table not in tables_used:
            tables_used.append(join_table)

    # ---------------------------------------------
    # COLUMNS USED
    # ---------------------------------------------

    columns_used = []

    if column:
        columns_used.append(column)

    if group_by and group_by not in columns_used:
        columns_used.append(group_by)

    if isinstance(filters, dict):
        for filter_column in filters:
            if filter_column not in columns_used:
                columns_used.append(filter_column)

    if isinstance(date_filter, dict):
        date_column = date_filter.get("column")

        if date_column and date_column not in columns_used:
            columns_used.append(date_column)

    if isinstance(join_config, dict):
        left_on = join_config.get("left_on")
        right_on = join_config.get("right_on")

        if left_on and left_on not in columns_used:
            columns_used.append(left_on)

        if right_on and right_on not in columns_used:
            columns_used.append(right_on)

    # ---------------------------------------------
    # EVIDENCE
    # ---------------------------------------------

    evidence = {
        "tables": tables_used,
        "rows_analyzed": execution_result.get(
            "rows_analyzed",
            0,
        ),
        "columns": columns_used,
        "filters": filters,
        "operation": operation,
    }

    # ---------------------------------------------
    # OPTIONAL DATE FILTER
    # ---------------------------------------------

    if date_filter:
        evidence["date_filter"] = date_filter

    # ---------------------------------------------
    # OPTIONAL JOIN
    # ---------------------------------------------

    if join_config:
        evidence["join"] = join_config

    return evidence


def run_verified_analysis(
    plan: dict,
    tables: dict,
) -> dict:
    """
    Run the complete execution + proof + verification pipeline.

    Flow:

        Plan
          ↓
        Executor
          ↓
        Answer
          ↓
        Proof Generator
          ↓
        Proof Code
          ↓
        Verifier
          ↓
        Final Result
    """

    # ---------------------------------------------
    # STEP 1 — EXECUTE THE PLAN
    # ---------------------------------------------

    execution_result = execute_plan(
        plan=plan,
        tables=tables,
    )

    # ---------------------------------------------
    # STOP IF EXECUTION DID NOT PRODUCE AN ANSWER
    # ---------------------------------------------

    if execution_result["status"] != "executed":
        return {
            "status": execution_result["status"],
            "answer": None,
            "proof_code": None,
            "verification": {
                "executed": False,
                "matched": False,
            },
            "evidence": _build_evidence(
                plan,
                execution_result,
            ),
            "reason": execution_result.get(
                "reason",
                "Execution did not produce an answer.",
            ),
        }

    # ---------------------------------------------
    # STEP 2 — GENERATE PROOF
    # ---------------------------------------------

    try:
        proof_code = generate_proof(plan)

    except Exception as exc:
        return {
            "status": "execution_error",
            "answer": execution_result.get("answer"),
            "proof_code": None,
            "verification": {
                "executed": False,
                "matched": False,
            },
            "evidence": _build_evidence(
                plan,
                execution_result,
            ),
            "reason": f"Proof generation failed: {exc}",
        }

    # ---------------------------------------------
    # STEP 3 — VERIFY THE PROOF
    # ---------------------------------------------

    verification_result = verify_proof(
        proof_code=proof_code,
        expected_result=execution_result["answer"],
        tables=tables,
    )

    # ---------------------------------------------
    # STEP 4 — FINAL STATUS
    # ---------------------------------------------

    if verification_result["status"] == "verified":
        final_status = "verified"
    else:
        final_status = "verification_failed"

    # ---------------------------------------------
    # STEP 5 — FINAL RESULT
    # ---------------------------------------------

    return {
        "status": final_status,
        "answer": execution_result["answer"],
        "proof_code": proof_code,
        "verification": {
            "executed": verification_result["executed"],
            "matched": verification_result["matched"],
        },
        "evidence": _build_evidence(
            plan,
            execution_result,
        ),
        "reason": verification_result.get(
            "reason",
            "",
        ),
    }