"""Member 2 - Plan schema (Contract B: Agent -> Executor)."""
from __future__ import annotations

from typing import Any, Dict, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator

SIMPLE_OPS = ("count", "sum", "average", "min", "max")
GROUP_OPS = ("group_count", "group_sum", "group_average", "group_min", "group_max")
ALL_OPS = SIMPLE_OPS + GROUP_OPS
NEEDS_COLUMN = ("sum", "average", "min", "max", "group_sum", "group_average", "group_min", "group_max")

Operation = Literal[
    "count", "sum", "average", "min", "max",
    "group_count", "group_sum", "group_average", "group_min", "group_max",
]


class DateFilter(BaseModel):
    """DATE FILTER. Use year (+ optional month) OR start/end (ISO dates)."""
    model_config = ConfigDict(extra="forbid")
    column: str
    year: Optional[int] = None
    month: Optional[int] = Field(default=None, ge=1, le=12)
    start: Optional[str] = None
    end: Optional[str] = None

    @model_validator(mode="after")
    def _check(self):
        has_range = self.start is not None or self.end is not None
        has_ym = self.year is not None or self.month is not None
        if not has_range and not has_ym:
            raise ValueError("date_filter needs year/month or start/end")
        if has_range and has_ym:
            raise ValueError("date_filter: use year/month OR start/end, not both")
        return self


class JoinSpec(BaseModel):
    """JOIN: left table is the plan's `table`."""
    model_config = ConfigDict(extra="forbid")
    table: str
    left_on: str
    right_on: str
    how: Literal["inner", "left"] = "inner"


class AnswerablePlan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["answerable"]
    operation: Operation
    table: str
    column: Optional[str] = None
    filters: Dict[str, Any] = Field(default_factory=dict)
    date_filter: Optional[DateFilter] = None
    group_by: Optional[str] = None
    sort: Optional[Literal["ascending", "descending"]] = None
    limit: Optional[int] = Field(default=None, ge=1)
    join: Optional[JoinSpec] = None

    @model_validator(mode="after")
    def _check(self):
        op = self.operation
        if op in NEEDS_COLUMN and not self.column:
            raise ValueError(f"operation '{op}' requires 'column'")
        if op in GROUP_OPS and not self.group_by:
            raise ValueError(f"operation '{op}' requires 'group_by'")
        if op in SIMPLE_OPS and self.group_by:
            raise ValueError(f"operation '{op}' must not have 'group_by'; use group_* instead")
        if (self.sort or self.limit) and op not in GROUP_OPS:
            raise ValueError("'sort'/'limit' only apply to group_* operations")
        return self


class CannotDeterminePlan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["cannot_determine"]
    reason: str = Field(min_length=1)


class ClarificationPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["clarification_required"]
    reason: str = Field(min_length=1)
    question: str = Field(min_length=1)


Plan = Union[AnswerablePlan, CannotDeterminePlan, ClarificationPlan]

_STATUS_TO_MODEL = {
    "answerable": AnswerablePlan,
    "cannot_determine": CannotDeterminePlan,
    "clarification_required": ClarificationPlan,
}


def parse_plan(data: Dict[str, Any]) -> Plan:
    """Dict -> Plan. Raises ValueError (incl. pydantic.ValidationError) if invalid."""
    if not isinstance(data, dict):
        raise ValueError("plan must be a JSON object")
    model = _STATUS_TO_MODEL.get(data.get("status"))
    if model is None:
        raise ValueError(f"unknown or missing status: {data.get('status')!r}")
    return model(**data)


def plan_to_dict(plan: Plan) -> Dict[str, Any]:
    """Plan -> clean dict for the executor (drops unset/None fields)."""
    return plan.model_dump(exclude_none=True)