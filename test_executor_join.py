import pandas as pd

from src.executor.executor import execute_plan


sales = pd.DataFrame({
    "product_id": [
        "P1",
        "P2",
        "P3",
        "P4"
    ],
    "revenue": [
        60000,
        30000,
        20000,
        10000
    ]
})


products = pd.DataFrame({
    "product_id": [
        "P1",
        "P2",
        "P3",
        "P5"
    ],
    "category": [
        "Electronics",
        "Electronics",
        "Office",
        "Furniture"
    ]
})


tables = {
    "sales": sales,
    "products": products
}


print("===================================")
print("EXECUTOR JOIN VALIDATION TESTS")
print("===================================")


# -----------------------------------
# TEST 1 — JOIN + FILTER + AVERAGE
# -----------------------------------

print("\nTEST 1 — JOIN + FILTER + AVERAGE")

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
        "right_on": "product_id"
    }
}

result = execute_plan(
    plan,
    tables
)

print(result)

assert result["status"] == "executed"
assert result["answer"] == 45000.0
assert result["rows_analyzed"] == 2

print("TEST 1 PASSED")


# -----------------------------------
# TEST 2 — MISSING JOIN TABLE
# -----------------------------------

print("\nTEST 2 — MISSING JOIN TABLE")

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "join": {
        "table": "customers",
        "left_on": "product_id",
        "right_on": "product_id"
    }
}

result = execute_plan(
    plan,
    tables
)

print(result)

assert result["status"] == "execution_error"

assert (
    result["reason"]
    == "Join table 'customers' does not exist."
)

print("TEST 2 PASSED")


# -----------------------------------
# TEST 3 — INVALID JOIN COLUMN
# -----------------------------------

print("\nTEST 3 — INVALID JOIN COLUMN")

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "join": {
        "table": "products",
        "left_on": "customer_id",
        "right_on": "product_id"
    }
}

result = execute_plan(
    plan,
    tables
)

print(result)

assert result["status"] == "execution_error"

assert (
    result["reason"]
    == "Left join column 'customer_id' does not exist."
)

print("TEST 3 PASSED")


# -----------------------------------
# TEST 4 — NO MATCHING ROWS
# -----------------------------------

print("\nTEST 4 — JOIN + FILTER WITH NO MATCH")

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "category": "Healthcare"
    },
    "join": {
        "table": "products",
        "left_on": "product_id",
        "right_on": "product_id"
    }
}

result = execute_plan(
    plan,
    tables
)

print(result)

assert result["status"] == "cannot_determine"
assert result["answer"] is None
assert result["rows_analyzed"] == 0

print("TEST 4 PASSED")


# -----------------------------------
# FINAL RESULT
# -----------------------------------

print("\n===================================")
print("ALL EXECUTOR JOIN TESTS PASSED")
print("===================================")