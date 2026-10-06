import pytest

from src.agent.plan_schema import parse_plan, plan_to_dict


def test_contract_simple():
    p = parse_plan({"status": "answerable", "operation": "average", "table": "sales",
                    "column": "revenue", "filters": {"category": "Electronics"}})
    assert plan_to_dict(p)["operation"] == "average"


def test_contract_grouped():
    p = parse_plan({"status": "answerable", "operation": "group_average", "table": "sales",
                    "column": "revenue", "group_by": "category",
                    "sort": "descending", "limit": 1})
    assert p.limit == 1


def test_contract_cannot_determine():
    p = parse_plan({"status": "cannot_determine", "reason": "Year 2035 not in data."})
    assert p.status == "cannot_determine"


def test_contract_clarification():
    p = parse_plan({"status": "clarification_required",
                    "reason": "January appears in multiple years.",
                    "question": "Which year do you mean?"})
    assert p.question


def test_count_needs_no_column():
    parse_plan({"status": "answerable", "operation": "count", "table": "sales"})


def test_date_filter_and_join():
    parse_plan({"status": "answerable", "operation": "sum", "table": "sales", "column": "revenue",
                "date_filter": {"column": "date", "year": 2024, "month": 1},
                "join": {"table": "products", "left_on": "pid", "right_on": "id"}})


@pytest.mark.parametrize("bad", [
    {"status": "answerable", "operation": "average", "table": "sales"},
    {"status": "answerable", "operation": "group_sum", "table": "s", "column": "r"},
    {"status": "answerable", "operation": "sum", "table": "s", "column": "r", "group_by": "c"},
    {"status": "answerable", "operation": "regression", "table": "s", "column": "r"},
    {"status": "answerable", "operation": "sum", "table": "s", "column": "r", "sql": "DROP"},
    {"status": "answerable", "operation": "sum", "table": "s", "column": "r", "limit": 3},
    {"status": "cannot_determine"},
    {"status": "maybe"},
    {"status": "answerable", "operation": "sum", "table": "s", "column": "r",
     "date_filter": {"column": "d"}},
    {"status": "answerable", "operation": "sum", "table": "s", "column": "r",
     "date_filter": {"column": "d", "year": 2024, "start": "2024-01-01"}},
])
def test_invalid_rejected(bad):
    with pytest.raises(ValueError):
        parse_plan(bad)


def test_non_dict_rejected():
    with pytest.raises(ValueError):
        parse_plan("average revenue")