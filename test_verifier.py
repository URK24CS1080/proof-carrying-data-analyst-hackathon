import pandas as pd

from src.executor.executor import execute_plan
from src.executor.proof_generator import generate_proof
from src.verifier.verifier import verify_proof


print("===================================")
print("VERIFIER TESTS")
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
    "category": [
        "Electronics",
        "Electronics",
        "Electronics",
        "Office",
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
    "product_name": [
        "Laptop",
        "Phone",
        "Monitor",
        "Notebook",
    ],
})

tables = {
    "sales": sales,
    "products": products,
}


# --------------------------------------------------
# TEST 1 — BASIC AVERAGE
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
}

execution_result = execute_plan(
    plan,
    tables,
)

assert execution_result["status"] == "executed"

expected_answer = execution_result["answer"]

proof = generate_proof(plan)

verification_result = verify_proof(
    proof_code=proof,
    expected_result=expected_answer,
    tables=tables,
)

print("\nTEST 1 — BASIC AVERAGE")
print("Expected:", expected_answer)
print("Verification:", verification_result)

assert verification_result["status"] == "verified"
assert verification_result["executed"] is True
assert verification_result["matched"] is True

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
        "category": "Electronics",
    },
}

execution_result = execute_plan(
    plan,
    tables,
)

assert execution_result["status"] == "executed"

expected_answer = execution_result["answer"]

proof = generate_proof(plan)

verification_result = verify_proof(
    proof_code=proof,
    expected_result=expected_answer,
    tables=tables,
)

print("\nTEST 2 — FILTER + AVERAGE")
print("Expected:", expected_answer)
print("Verification:", verification_result)

assert verification_result["status"] == "verified"
assert verification_result["matched"] is True

print("TEST 2 PASSED")


# --------------------------------------------------
# TEST 3 — WRONG PROOF RESULT
# --------------------------------------------------

wrong_proof = """
answer = 999999
print(answer)
"""

verification_result = verify_proof(
    proof_code=wrong_proof,
    expected_result=30000.0,
    tables=tables,
)

print("\nTEST 3 — WRONG PROOF RESULT")
print("Verification:", verification_result)

assert verification_result["status"] == "verification_failed"
assert verification_result["executed"] is True
assert verification_result["matched"] is False

print("TEST 3 PASSED")


# --------------------------------------------------
# TEST 4 — BROKEN PROOF
# --------------------------------------------------

broken_proof = """
answer = df_that_does_not_exist["revenue"].mean()
print(answer)
"""

verification_result = verify_proof(
    proof_code=broken_proof,
    expected_result=30000.0,
    tables=tables,
)

print("\nTEST 4 — BROKEN PROOF")
print("Verification:", verification_result)

assert verification_result["status"] == "verification_failed"
assert verification_result["executed"] is False
assert verification_result["matched"] is False

print("TEST 4 PASSED")


# --------------------------------------------------
# TEST 5 — PROOF WITHOUT ANSWER VARIABLE
# --------------------------------------------------

missing_answer_proof = """
value = 30000
print(value)
"""

verification_result = verify_proof(
    proof_code=missing_answer_proof,
    expected_result=30000.0,
    tables=tables,
)

print("\nTEST 5 — MISSING ANSWER VARIABLE")
print("Verification:", verification_result)

assert verification_result["status"] == "verification_failed"
assert verification_result["executed"] is True
assert verification_result["matched"] is False

print("TEST 5 PASSED")


# --------------------------------------------------
# TEST 6 — GROUP AVERAGE
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
    "group_by": "category",
    "sort": "descending",
    "limit": 2,
}

execution_result = execute_plan(
    plan,
    tables,
)

assert execution_result["status"] == "executed"

expected_answer = execution_result["answer"]

proof = generate_proof(plan)

verification_result = verify_proof(
    proof_code=proof,
    expected_result=expected_answer,
    tables=tables,
)

print("\nTEST 6 — GROUP AVERAGE")
print("Expected:")
print(expected_answer)
print("Verification:", verification_result)

assert verification_result["status"] == "verified"
assert verification_result["matched"] is True

print("TEST 6 PASSED")


# --------------------------------------------------
# TEST 7 — JOIN + FILTER + AVERAGE
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "product_name": "Laptop",
    },
    "join": {
        "table": "products",
        "left_on": "product_id",
        "right_on": "product_id",
    },
}

execution_result = execute_plan(
    plan,
    tables,
)

assert execution_result["status"] == "executed"

expected_answer = execution_result["answer"]

proof = generate_proof(plan)

verification_result = verify_proof(
    proof_code=proof,
    expected_result=expected_answer,
    tables=tables,
)

print("\nTEST 7 — JOIN + FILTER + AVERAGE")
print("Expected:", expected_answer)
print("Verification:", verification_result)

assert verification_result["status"] == "verified"
assert verification_result["matched"] is True

print("TEST 7 PASSED")


print("\n===================================")
print("ALL VERIFIER TESTS PASSED")
print("===================================")