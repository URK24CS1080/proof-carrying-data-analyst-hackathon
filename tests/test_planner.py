import json

from src.agent.llm_client import MockLLM
from src.agent.planner import extract_json, make_plan

SCHEMA = {"tables": [{"name": "sales", "rows": 100,
          "columns": {"category": "string", "revenue": "float", "date": "datetime"},
          "missing_values": {}, "duplicate_rows": 0, "years": [2023, 2024]}]}


def plan_for(resp, q="q"):
    return make_plan(q, SCHEMA, MockLLM([resp]))


GOOD = json.dumps({"status": "answerable", "operation": "average", "table": "sales",
                   "column": "revenue", "filters": {"category": "Electronics"}})


def test_good_plan():
    assert plan_for(GOOD).status == "answerable"


def test_fenced_json():
    assert plan_for("```json\n" + GOOD + "\n```").status == "answerable"


def test_prose_around_json():
    assert plan_for("Sure! Here is the plan: " + GOOD + " Hope it helps.").status == "answerable"


def test_garbage_becomes_refusal():
    r = plan_for("I think the answer is 42")
    assert r.status == "cannot_determine"


def test_invalid_operation_becomes_refusal():
    bad = json.dumps({"status": "answerable", "operation": "regression", "table": "sales", "column": "revenue"})
    assert plan_for(bad).status == "cannot_determine"


def test_hallucinated_column_becomes_refusal():
    bad = json.dumps({"status": "answerable", "operation": "sum", "table": "sales", "column": "profit"})
    assert plan_for(bad).status == "cannot_determine"


def test_year_trap_through_pipeline():
    r = plan_for(json.dumps({"status": "answerable", "operation": "sum", "table": "sales",
                             "column": "revenue", "date_filter": {"column": "date", "year": 2035}}))
    assert r.status == "cannot_determine" and "2035" in r.reason


def test_llm_refusal_passes():
    r = plan_for(json.dumps({"status": "cannot_determine", "reason": "no such data"}))
    assert r.status == "cannot_determine"


def test_llm_error_handled():
    class Boom:
        def complete(self, s, u):
            raise RuntimeError("quota")
    assert make_plan("q", SCHEMA, Boom()).status == "cannot_determine"


def test_empty_question_and_no_tables():
    assert make_plan("  ", SCHEMA, MockLLM(["{}"])).status == "cannot_determine"
    assert make_plan("q", {"tables": []}, MockLLM(["{}"])).status == "cannot_determine"


def test_prompt_contains_schema_and_question():
    llm = MockLLM([GOOD])
    make_plan("Average revenue for Electronics?", SCHEMA, llm)
    system, user = llm.calls[0]
    assert "revenue" in user and "Average revenue for Electronics?" in user
    assert "JSON" in system


def test_extract_json_rejects_non_object():
    import pytest
    with pytest.raises(ValueError):
        extract_json("[1,2,3]")