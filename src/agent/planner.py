"""Member 2 - Planner entry point.

make_plan(question, schema, llm) -> Plan
  1. build prompt  2. call LLM  3. extract JSON  4. parse_plan  5. validate_plan
Never raises: any failure becomes a CannotDeterminePlan with a clear reason.
"""
import json
import re
from typing import Any, Dict

from .llm_client import LLMClient
from .plan_schema import CannotDeterminePlan, Plan, parse_plan
from .prompts import SYSTEM_PROMPT, build_user_prompt
from .validate_plan import validate_plan


def _cant(reason: str) -> CannotDeterminePlan:
    return CannotDeterminePlan(status="cannot_determine", reason=reason)


def extract_json(text: str) -> Dict[str, Any]:
    """Pull the first JSON object out of LLM text (handles ```json fences / extra prose)."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        if start == -1:
            raise ValueError("no JSON object found in LLM response")
        obj, _ = json.JSONDecoder().raw_decode(text[start:])
    if not isinstance(obj, dict):
        raise ValueError("LLM response JSON is not an object")
    return obj


def make_plan(question: str, schema: Dict[str, Any], llm: LLMClient) -> Plan:
    if not question or not question.strip():
        return _cant("Empty question.")
    if not schema.get("tables"):
        return _cant("No data tables are loaded.")
    try:
        raw = llm.complete(SYSTEM_PROMPT, build_user_prompt(question, schema))
    except Exception as e:  # network, auth, quota...
        return _cant(f"The language model could not be reached: {e}")
    try:
        plan = parse_plan(extract_json(raw))
    except Exception as e:
        return _cant(f"The model returned an invalid plan, so no answer was attempted: {e}")
    return validate_plan(plan, schema)