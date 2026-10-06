import pandas as pd

from src.executor.pipeline import run_verified_analysis


print("===================================")
print("PIPELINE TESTS")
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

result = run_verified_analysis(
    plan=plan,
    tables=tables,
)

print("\nTEST 1 — BASIC AVERAGE")
print("Status:", result["status"])
print("Answer:", result["answer"])
print("Verification:", result["verification"])

assert result["status"] == "verified"
assert result["answer"] == 30000.0
assert result["verification"]["executed"] is True
assert result["verification"]["matched"] is True
assert result["proof_code"] is not None

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

result = run_verified_analysis(
    plan=plan,
    tables=tables,
)

print("\nTEST 2 — FILTER + AVERAGE")
print("Status:", result["status"])
print("Answer:", result["answer"])
print("Verification:", result["verification"])

assert result["status"] == "verified"
assert abs(
    result["answer"] - 36666.666666666664
) < 1e-9

assert result["verification"]["matched"] is True

print("TEST 2 PASSED")


# --------------------------------------------------
# TEST 3 — GROUP AVERAGE
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

result = run_verified_analysis(
    plan=plan,
    tables=tables,
)

print("\nTEST 3 — GROUP AVERAGE")
print("Status:", result["status"])
print("Answer:")
print(result["answer"])
print("Verification:", result["verification"])

assert result["status"] == "verified"
assert result["verification"]["matched"] is True

assert result["answer"].iloc[0]["category"] == "Electronics"

print("TEST 3 PASSED")


# --------------------------------------------------
# TEST 4 — JOIN + FILTER + AVERAGE
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

result = run_verified_analysis(
    plan=plan,
    tables=tables,
)

print("\nTEST 4 — JOIN + FILTER + AVERAGE")
print("Status:", result["status"])
print("Answer:", result["answer"])
print("Verification:", result["verification"])

assert result["status"] == "verified"
assert result["answer"] == 20000.0
assert result["verification"]["matched"] is True

print("TEST 4 PASSED")


# --------------------------------------------------
# TEST 5 — NO MATCHING ROWS
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "category": "NonExistingCategory",
    },
}

result = run_verified_analysis(
    plan=plan,
    tables=tables,
)

print("\nTEST 5 — NO MATCHING ROWS")
print("Status:", result["status"])
print("Answer:", result["answer"])
print("Reason:", result["reason"])

assert result["status"] == "cannot_determine"
assert result["answer"] is None
assert result["proof_code"] is None

print("TEST 5 PASSED")


# --------------------------------------------------
# TEST 6 — PLAN ALREADY CANNOT DETERMINE
# --------------------------------------------------

plan = {
    "status": "cannot_determine",
    "reason": "Requested year does not exist.",
}

result = run_verified_analysis(
    plan=plan,
    tables=tables,
)

print("\nTEST 6 — CANNOT DETERMINE PLAN")
print("Status:", result["status"])
print("Answer:", result["answer"])
print("Reason:", result["reason"])

assert result["status"] == "cannot_determine"
assert result["answer"] is None
assert result["proof_code"] is None

print("TEST 6 PASSED")


print("\n===================================")
print("ALL PIPELINE TESTS PASSED")
print("===================================")