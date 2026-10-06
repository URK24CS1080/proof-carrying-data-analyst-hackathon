from src.agent.plan_schema import parse_plan
from src.agent.validate_plan import validate_plan

SCHEMA = {"tables": [
    {"name": "sales", "rows": 100,
     "columns": {"product": "string", "category": "string", "revenue": "float",
                 "date": "datetime", "qty": "int"},
     "missing_values": {}, "duplicate_rows": 0, "years": [2023, 2024]},
    {"name": "products", "rows": 10, "columns": {"id": "int", "name": "string"},
     "missing_values": {}, "duplicate_rows": 0},
]}


def run(d):
    return validate_plan(parse_plan(d), SCHEMA)


def base(**kw):
    d = {"status": "answerable", "operation": "average", "table": "sales", "column": "revenue"}
    d.update(kw)
    return d


def test_valid_passes():
    assert run(base(filters={"category": "Electronics"})).status == "answerable"


def test_unknown_table():
    r = run(base(table="orders"))
    assert r.status == "cannot_determine" and "orders" in r.reason


def test_unknown_column():
    assert run(base(column="profit")).status == "cannot_determine"


def test_unknown_filter_column():
    assert run(base(filters={"region": "EU"})).status == "cannot_determine"


def test_average_of_string_refused():
    assert run(base(column="product")).status == "cannot_determine"


def test_max_of_datetime_ok():
    assert run(base(operation="max", column="date")).status == "answerable"


def test_year_2035_trap():
    r = run(base(date_filter={"column": "date", "year": 2035}))
    assert r.status == "cannot_determine" and "2035" in r.reason


def test_year_exists_ok():
    assert run(base(date_filter={"column": "date", "year": 2024})).status == "answerable"


def test_month_without_year_asks():
    r = run(base(date_filter={"column": "date", "month": 1}))
    assert r.status == "clarification_required" and r.question


def test_date_filter_on_non_date_column():
    assert run(base(date_filter={"column": "product", "year": 2024})).status == "cannot_determine"


def test_group_by_unknown():
    r = run({"status": "answerable", "operation": "group_sum", "table": "sales",
             "column": "revenue", "group_by": "region"})
    assert r.status == "cannot_determine"


def test_join_ok_and_bad():
    j = {"table": "products", "left_on": "qty", "right_on": "id"}
    assert run(base(join=j)).status == "answerable"
    assert run(base(join={**j, "right_on": "zzz"})).status == "cannot_determine"
    assert run(base(join={**j, "table": "nope"})).status == "cannot_determine"


def test_refusal_passes_through():
    r = run({"status": "cannot_determine", "reason": "x"})
    assert r.status == "cannot_determine"