import io
from contextlib import redirect_stdout

import pandas as pd

from src.executor.executor import execute_plan
from src.executor.proof_generator import generate_proof


print("===================================")
print("GROUP PROOF GENERATOR TESTS")
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
    ],
    "category": [
        "Electronics",
        "Electronics",
        "Office",
        "Electronics",
    ],
    "revenue": [
        20000,
        30000,
        10000,
        60000,
    ],
})

tables = {
    "sales": sales
}


# --------------------------------------------------
# TEST 1 — GROUP AVERAGE
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
    "group_by": "category",
}

proof = generate_proof(plan)

print("\nTEST 1 — GROUP AVERAGE")
print(proof)

assert "groupby('category'" in proof
assert "['revenue']" in proof
assert "reset_index(name='average')" in proof
assert "answer = df" in proof

print("TEST 1 PASSED")


# --------------------------------------------------
# TEST 2 — GROUP AVERAGE + SORT DESCENDING
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
    "group_by": "category",
    "sort": "descending",
}

proof = generate_proof(plan)

print("\nTEST 2 — GROUP AVERAGE + SORT DESCENDING")
print(proof)

assert "ascending=False" in proof
assert "by='average'" in proof

print("TEST 2 PASSED")


# --------------------------------------------------
# TEST 3 — GROUP AVERAGE + SORT + TOP 1
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
    "group_by": "category",
    "sort": "descending",
    "limit": 1,
}

proof = generate_proof(plan)

print("\nTEST 3 — GROUP AVERAGE + SORT + TOP 1")
print(proof)

assert "ascending=False" in proof
assert "df = df.head(1).copy()" in proof

print("TEST 3 PASSED")


# --------------------------------------------------
# TEST 4 — ACTUAL PROOF EXECUTION
# --------------------------------------------------

execution_result = execute_plan(
    plan,
    tables
)

assert execution_result["status"] == "executed"

expected_result = execution_result["answer"]

proof = generate_proof(plan)

namespace = {
    "tables": tables
}

output = io.StringIO()

with redirect_stdout(output):
    exec(proof, namespace)

proof_result = namespace["answer"]

print("\nTEST 4 — ACTUAL PROOF EXECUTION")
print("Executor result:")
print(expected_result)

print("\nProof result:")
print(proof_result)

assert expected_result.reset_index(drop=True).equals(
    proof_result.reset_index(drop=True)
)

print("TEST 4 PASSED")


print("\n===================================")
print("ALL GROUP PROOF TESTS PASSED")
print("===================================")