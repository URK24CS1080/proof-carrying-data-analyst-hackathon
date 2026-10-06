import io
from contextlib import redirect_stdout

import pandas as pd

from src.executor.executor import execute_plan
from src.executor.proof_generator import generate_proof


print("===================================")
print("PROOF EXECUTION TESTS")
print("===================================")


# --------------------------------------------------
# TEST DATA
# --------------------------------------------------

sales = pd.DataFrame({
    "product": ["Laptop", "Phone", "Chair", "Monitor"],
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
# TEST 1 — AVERAGE
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
}

execution_result = execute_plan(
    plan,
    tables
)

assert execution_result["status"] == "executed"

expected_answer = execution_result["answer"]

proof_code = generate_proof(plan)

namespace = {
    "tables": tables
}

output = io.StringIO()

with redirect_stdout(output):
    exec(proof_code, namespace)

proof_answer = float(output.getvalue().strip())

print("TEST 1 — AVERAGE")
print("Executor answer:", expected_answer)
print("Proof answer:", proof_answer)

assert abs(expected_answer - proof_answer) < 1e-9

print("TEST 1 PASSED")


# --------------------------------------------------
# TEST 2 — FILTER + AVERAGE
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "category": "Electronics"
    }
}

execution_result = execute_plan(
    plan,
    tables
)

assert execution_result["status"] == "executed"

expected_answer = execution_result["answer"]

proof_code = generate_proof(plan)

namespace = {
    "tables": tables
}

output = io.StringIO()

with redirect_stdout(output):
    exec(proof_code, namespace)

proof_answer = float(output.getvalue().strip())

print("\nTEST 2 — FILTER + AVERAGE")
print("Executor answer:", expected_answer)
print("Proof answer:", proof_answer)

assert abs(expected_answer - proof_answer) < 1e-9

print("TEST 2 PASSED")


# --------------------------------------------------
# TEST 3 — COUNT
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "count",
    "table": "sales",
    "column": "product",
}

execution_result = execute_plan(
    plan,
    tables
)

assert execution_result["status"] == "executed"

expected_answer = execution_result["answer"]

proof_code = generate_proof(plan)

namespace = {
    "tables": tables
}

output = io.StringIO()

with redirect_stdout(output):
    exec(proof_code, namespace)

proof_answer = int(float(output.getvalue().strip()))

print("\nTEST 3 — COUNT")
print("Executor answer:", expected_answer)
print("Proof answer:", proof_answer)

assert expected_answer == proof_answer

print("TEST 3 PASSED")


# --------------------------------------------------
# TEST 4 — SUM
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "sum",
    "table": "sales",
    "column": "revenue",
}

execution_result = execute_plan(
    plan,
    tables
)

assert execution_result["status"] == "executed"

expected_answer = execution_result["answer"]

proof_code = generate_proof(plan)

namespace = {
    "tables": tables
}

output = io.StringIO()

with redirect_stdout(output):
    exec(proof_code, namespace)

proof_answer = float(output.getvalue().strip())

print("\nTEST 4 — SUM")
print("Executor answer:", expected_answer)
print("Proof answer:", proof_answer)

assert abs(expected_answer - proof_answer) < 1e-9

print("TEST 4 PASSED")


# --------------------------------------------------
# TEST 5 — MIN
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "min",
    "table": "sales",
    "column": "revenue",
}

execution_result = execute_plan(
    plan,
    tables
)

assert execution_result["status"] == "executed"

expected_answer = execution_result["answer"]

proof_code = generate_proof(plan)

namespace = {
    "tables": tables
}

output = io.StringIO()

with redirect_stdout(output):
    exec(proof_code, namespace)

proof_answer = float(output.getvalue().strip())

print("\nTEST 5 — MIN")
print("Executor answer:", expected_answer)
print("Proof answer:", proof_answer)

assert abs(expected_answer - proof_answer) < 1e-9

print("TEST 5 PASSED")


# --------------------------------------------------
# TEST 6 — MAX
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "max",
    "table": "sales",
    "column": "revenue",
}

execution_result = execute_plan(
    plan,
    tables
)

assert execution_result["status"] == "executed"

expected_answer = execution_result["answer"]

proof_code = generate_proof(plan)

namespace = {
    "tables": tables
}

output = io.StringIO()

with redirect_stdout(output):
    exec(proof_code, namespace)

proof_answer = float(output.getvalue().strip())

print("\nTEST 6 — MAX")
print("Executor answer:", expected_answer)
print("Proof answer:", proof_answer)

assert abs(expected_answer - proof_answer) < 1e-9

print("TEST 6 PASSED")


print("\n===================================")
print("ALL PROOF EXECUTION TESTS PASSED")
print("===================================")