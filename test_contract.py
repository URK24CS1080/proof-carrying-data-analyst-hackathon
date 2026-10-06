import pandas as pd

from src.executor.pipeline import run_verified_analysis


print("===================================")
print("FINAL CONTRACT TEST")
print("===================================")


sales = pd.DataFrame({
    "category": [
        "Electronics",
        "Electronics",
        "Office",
        "Office",
    ],
    "revenue": [
        20000,
        30000,
        10000,
        15000,
    ],
})


tables = {
    "sales": sales,
}


# --------------------------------------------------
# TEST 1 — VERIFIED RESULT CONTRACT
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "category": "Electronics"
    },
}


result = run_verified_analysis(
    plan,
    tables,
)


print("\nTEST 1 — VERIFIED RESULT")
print(result)


assert result["status"] == "verified"

assert result["answer"] == 25000.0

assert isinstance(result["proof_code"], str)

assert result["proof_code"].strip() != ""

assert result["verification"]["executed"] is True

assert result["verification"]["matched"] is True

assert isinstance(result["evidence"], dict)

assert result["evidence"]["tables"] == [
    "sales"
]

assert result["evidence"]["rows_analyzed"] == 2

assert result["evidence"]["columns"] == [
    "revenue",
    "category",
]

assert result["evidence"]["filters"] == {
    "category": "Electronics"
}

assert result["evidence"]["operation"] == "average"

assert isinstance(result["reason"], str)

assert result["reason"] != ""

print("TEST 1 PASSED")


# --------------------------------------------------
# TEST 2 — CANNOT DETERMINE CONTRACT
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "category": "NonExistingCategory"
    },
}


result = run_verified_analysis(
    plan,
    tables,
)


print("\nTEST 2 — CANNOT DETERMINE RESULT")
print(result)


assert result["status"] == "cannot_determine"

assert result["answer"] is None

assert result["proof_code"] is None

assert result["verification"]["executed"] is False

assert result["verification"]["matched"] is False

assert isinstance(result["evidence"], dict)

assert result["evidence"]["tables"] == [
    "sales"
]

assert result["evidence"]["rows_analyzed"] == 0

assert result["evidence"]["filters"] == {
    "category": "NonExistingCategory"
}

assert result["reason"] != ""

print("TEST 2 PASSED")


# --------------------------------------------------
# TEST 3 — CANNOT DETERMINE PLAN CONTRACT
# --------------------------------------------------

plan = {
    "status": "cannot_determine",
    "reason": "Requested year does not exist.",
}


result = run_verified_analysis(
    plan,
    tables,
)


print("\nTEST 3 — CANNOT DETERMINE PLAN")
print(result)


assert result["status"] == "cannot_determine"

assert result["answer"] is None

assert result["proof_code"] is None

assert result["verification"]["executed"] is False

assert result["verification"]["matched"] is False

assert result["reason"] == "Requested year does not exist."

assert isinstance(result["evidence"], dict)

print("TEST 3 PASSED")


# --------------------------------------------------
# FINAL RESULT
# --------------------------------------------------

print("\n===================================")
print("ALL FINAL CONTRACT TESTS PASSED")
print("===================================")