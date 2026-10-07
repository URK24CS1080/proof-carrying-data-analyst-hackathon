"""Member 2 - interactive demo: type a question -> real LLM -> plan -> validation.

Run with the built-in sample schema:   python demo_planner.py
Run on your own CSV file(s):           python demo_planner.py data/sales.csv data/products.csv

NOTE: build_stub_schema() is a TEMPORARY stand-in for Member 1's data module (Contract A).
It exists only so this demo can run on a real file. Member 1's loader replaces it.
"""
import json
import os
import sys

from src.agent.llm_client import get_llm
from src.agent.planner import make_plan

SAMPLE_SCHEMA = {"tables": [
    {"name": "sales", "rows": 1248,
     "columns": {"product": "string", "category": "string", "revenue": "float",
                 "date": "datetime", "quantity": "int"},
     "missing_values": {"revenue": 4}, "duplicate_rows": 12,
     "years": [2023, 2024],
     "samples": {"category": ["Electronics", "Clothing", "Home"]}},
]}


def build_stub_schema(paths):
    import pandas as pd  # only needed for this temporary helper

    tables = []
    for p in paths:
        df = pd.read_csv(p)
        cols, years, samples = {}, set(), {}
        for c in df.columns:
            s = df[c]
            if "date" in str(c).lower() or "time" in str(c).lower():
                parsed = pd.to_datetime(s, errors="coerce")
                if parsed.notna().mean() > 0.9:
                    cols[c] = "datetime"
                    years |= set(int(y) for y in parsed.dropna().dt.year.unique())
                    continue
            if pd.api.types.is_integer_dtype(s):
                cols[c] = "int"
            elif pd.api.types.is_float_dtype(s):
                cols[c] = "float"
            else:
                cols[c] = "string"
                uniq = s.dropna().astype(str).unique()
                if len(uniq) <= 30:
                    samples[c] = sorted(uniq.tolist())
        table = {
            "name": os.path.splitext(os.path.basename(p))[0],
            "rows": int(len(df)),
            "columns": {str(k): v for k, v in cols.items()},
            "missing_values": {str(k): int(v) for k, v in df.isna().sum().items() if v},
            "duplicate_rows": int(df.duplicated().sum()),
        }
        if years:
            table["years"] = sorted(years)
        if samples:
            table["samples"] = {str(k): v for k, v in samples.items()}
        tables.append(table)
    return {"tables": tables}


def main():
    schema = build_stub_schema(sys.argv[1:]) if len(sys.argv) > 1 else SAMPLE_SCHEMA
    print("Tables loaded:")
    for t in schema["tables"]:
        print(f"  - {t['name']}: {t['rows']} rows, columns = {list(t['columns'])}")
    llm = get_llm()
    print("\nType a question (or 'quit' to exit).")
    while True:
        try:
            q = input("\nQuestion> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q.lower() in ("quit", "exit", "q"):
            break
        if not q:
            continue
        plan = make_plan(q, schema, llm)
        print(f"\nSTATUS: {plan.status.upper()}")
        if plan.status == "cannot_determine":
            print(f"REASON: {plan.reason}")
        elif plan.status == "clarification_required":
            print(f"REASON: {plan.reason}\nASK USER: {plan.question}")
        print(json.dumps(plan.model_dump(exclude_none=True), indent=2))


if __name__ == "__main__":
    main()
    