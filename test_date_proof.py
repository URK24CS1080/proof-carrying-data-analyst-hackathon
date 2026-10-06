import io
from contextlib import redirect_stdout

import pandas as pd

from src.executor.executor import execute_plan
from src.executor.proof_generator import generate_proof


print("===================================")
print("DATE PROOF TESTS")
print("===================================")


# --------------------------------------------------
# TEST DATA
# --------------------------------------------------

sales = pd.DataFrame({
    "product": [
        "Laptop",
        "Phone",
        "Chair",
        "Monitor",
        "Keyboard",
    ],
    "category": [
        "Electronics",
        "Electronics",
        "Office",
        "Electronics",
        "Electronics",
    ],
    "revenue": [
        20000,
        30000,
        10000,
        60000,
        15000,
    ],
    "date": [
        "2025-01-10",
        "2025-05-15",
        "2025-07-20",
        "2025-12-01",
        "2026-01-10",
    ],
})

tables = {
    "sales": sales
}


# --------------------------------------------------
# TEST 1 — DATE FILTER + SUM
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "sum",
    "table": "sales",
    "column": "revenue",
    "date_filter": {
        "column": "date",
        "start": "2025-01-01",
        "end": "2025-12-31",
    },
}

proof = generate_proof(plan)

print("\nTEST 1 — DATE FILTER + SUM")
print(proof)

assert "to_datetime" in proof
assert "2025-01-01" in proof
assert "2025-12-31" in proof
assert "dropna().sum()" in proof

print("TEST 1 PASSED")


# --------------------------------------------------
# TEST 2 — ACTUAL PROOF EXECUTION
# --------------------------------------------------

execution_result = execute_plan(
    plan,
    tables
)

assert execution_result["status"] == "executed"

expected_answer = execution_result["answer"]

namespace = {
    "tables": tables
}

output = io.StringIO()

with redirect_stdout(output):
    exec(proof, namespace)

proof_answer = float(
    output.getvalue().strip()
)

print("\nTEST 2 — ACTUAL PROOF EXECUTION")
print("Executor answer:", expected_answer)
print("Proof answer:", proof_answer)

assert abs(
    expected_answer - proof_answer
) < 1e-9

print("TEST 2 PASSED")


# --------------------------------------------------
# TEST 3 — DATE FILTER + CATEGORY FILTER + AVERAGE
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "category": "Electronics"
    },
    "date_filter": {
        "column": "date",
        "start": "2025-01-01",
        "end": "2025-12-31",
    },
}

proof = generate_proof(plan)

print("\nTEST 3 — DATE FILTER + CATEGORY FILTER + AVERAGE")
print(proof)

execution_result = execute_plan(
    plan,
    tables
)

assert execution_result["status"] == "executed"

expected_answer = execution_result["answer"]

namespace = {
    "tables": tables
}

output = io.StringIO()

with redirect_stdout(output):
    exec(proof, namespace)

proof_answer = float(
    output.getvalue().strip()
)

print("Executor answer:", expected_answer)
print("Proof answer:", proof_answer)

assert abs(
    expected_answer - proof_answer
) < 1e-9

print("TEST 3 PASSED")


# --------------------------------------------------
# TEST 4 — ONLY START DATE
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "count",
    "table": "sales",
    "column": "product",
    "date_filter": {
        "column": "date",
        "start": "2026-01-01",
    },
}

proof = generate_proof(plan)

print("\nTEST 4 — START DATE ONLY")
print(proof)

execution_result = execute_plan(
    plan,
    tables
)

assert execution_result["status"] == "executed"

expected_answer = execution_result["answer"]

namespace = {
    "tables": tables
}

output = io.StringIO()

with redirect_stdout(output):
    exec(proof, namespace)

proof_answer = int(
    float(output.getvalue().strip())
)

print("Executor answer:", expected_answer)
print("Proof answer:", proof_answer)

assert expected_answer == proof_answer

print("TEST 4 PASSED")


# --------------------------------------------------
# TEST 5 — INVALID DATE FILTER
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "sum",
    "table": "sales",
    "column": "revenue",
    "date_filter": {
        "start": "2025-01-01",
        "end": "2025-12-31",
    },
}

try:

    generate_proof(plan)

    assert False, (
        "Expected ValueError for missing "
        "date column."
    )

except ValueError as exc:

    print("\nTEST 5 — INVALID DATE FILTER")
    print(exc)

    assert (
        "Date filter requires 'column'."
        in str(exc)
    )

print("TEST 5 PASSED")


print("\n===================================")
print("ALL DATE PROOF TESTS PASSED")
print("===================================")