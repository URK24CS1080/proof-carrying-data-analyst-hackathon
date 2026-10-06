import io
from contextlib import redirect_stdout

import pandas as pd

from src.executor.executor import execute_plan
from src.executor.proof_generator import generate_proof


print("===================================")
print("JOIN PROOF TESTS")
print("===================================")


# --------------------------------------------------
# TEST DATA
# --------------------------------------------------

sales = pd.DataFrame({
    "product_id": [
        "P1",
        "P2",
        "P3",
        "P4",
    ],
    "revenue": [
        20000,
        30000,
        60000,
        10000,
    ],
})

products = pd.DataFrame({
    "product_id": [
        "P1",
        "P2",
        "P3",
        "P4",
    ],
    "category": [
        "Electronics",
        "Electronics",
        "Electronics",
        "Office",
    ],
})

tables = {
    "sales": sales,
    "products": products,
}


# --------------------------------------------------
# TEST 1 — BASIC JOIN + AVERAGE
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "join": {
        "table": "products",
        "left_on": "product_id",
        "right_on": "product_id",
    },
}

proof = generate_proof(plan)

print("\nTEST 1 — JOIN + AVERAGE")
print(proof)

assert "tables['products']" in proof
assert "left_on='product_id'" in proof
assert "right_on='product_id'" in proof
assert 'how="inner"' in proof
assert "dropna().mean()" in proof

print("TEST 1 PASSED")


# --------------------------------------------------
# TEST 2 — ACTUAL JOIN PROOF EXECUTION
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

print("\nTEST 2 — ACTUAL JOIN PROOF EXECUTION")
print("Executor answer:", expected_answer)
print("Proof answer:", proof_answer)

assert abs(
    expected_answer - proof_answer
) < 1e-9

print("TEST 2 PASSED")


# --------------------------------------------------
# TEST 3 — JOIN + FILTER + AVERAGE
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "category": "Electronics"
    },
    "join": {
        "table": "products",
        "left_on": "product_id",
        "right_on": "product_id",
    },
}

proof = generate_proof(plan)

print("\nTEST 3 — JOIN + FILTER + AVERAGE")
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
# TEST 4 — INVALID JOIN TYPE
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "join": {
        "table": "products",
        "left_on": "product_id",
        "right_on": "product_id",
        "how": "left",
    },
}

try:

    generate_proof(plan)

    assert False, (
        "Expected ValueError for "
        "unsupported JOIN type."
    )

except ValueError as exc:

    print("\nTEST 4 — INVALID JOIN TYPE")
    print(exc)

    assert (
        "Only 'inner' JOIN is supported."
        in str(exc)
    )

print("TEST 4 PASSED")


# --------------------------------------------------
# TEST 5 — MISSING JOIN TABLE
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "join": {
        "left_on": "product_id",
        "right_on": "product_id",
    },
}

try:

    generate_proof(plan)

    assert False, (
        "Expected ValueError for "
        "missing JOIN table."
    )

except ValueError as exc:

    print("\nTEST 5 — MISSING JOIN TABLE")
    print(exc)

    assert (
        "Join configuration requires 'table'."
        in str(exc)
    )

print("TEST 5 PASSED")


print("\n===================================")
print("ALL JOIN PROOF TESTS PASSED")
print("===================================")