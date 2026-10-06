import pandas as pd

from src.executor.executor import execute_plan


sales = pd.DataFrame({
    "product": [
        "Laptop",
        "Phone",
        "Tablet",
        "Monitor",
        "Chair",
        "Desk",
        "Shirt",
        "Jeans"
    ],
    "category": [
        "Electronics",
        "Electronics",
        "Electronics",
        "Office",
        "Furniture",
        "Furniture",
        "Clothing",
        "Clothing"
    ],
    "revenue": [
        60000,
        30000,
        20000,
        10000,
        30000,
        30000,
        20000,
        20000
    ]
})


tables = {
    "sales": sales
}


print("===================================")
print("EXECUTOR SORT + TOP N TESTS")
print("===================================")


# -----------------------------------
# TEST 1 — GROUP + SORT DESCENDING
# -----------------------------------

print("\nTEST 1 — GROUP + SORT DESCENDING")

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
    "group_by": "category",
    "sort": "descending"
}

result = execute_plan(
    plan,
    tables
)

print(result)

assert result["status"] == "executed"

answer = result["answer"]

assert answer.iloc[0]["category"] == "Electronics"

print("TEST 1 PASSED")


# -----------------------------------
# TEST 2 — GROUP + SORT + TOP 1
# -----------------------------------

print("\nTEST 2 — GROUP + SORT + TOP 1")

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
    "group_by": "category",
    "sort": "descending",
    "limit": 1
}

result = execute_plan(
    plan,
    tables
)

print(result)

assert result["status"] == "executed"

answer = result["answer"]

assert len(answer) == 1

assert answer.iloc[0]["category"] == "Electronics"

assert abs(
    answer.iloc[0]["average"] - 36666.666666666664
) < 0.000001

assert result["sort"] == "descending"

assert result["limit"] == 1

print("TEST 2 PASSED")


# -----------------------------------
# TEST 3 — ASCENDING + TOP 1
# -----------------------------------

print("\nTEST 3 — GROUP + SORT ASCENDING + TOP 1")

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
    "group_by": "category",
    "sort": "ascending",
    "limit": 1
}

result = execute_plan(
    plan,
    tables
)

print(result)

assert result["status"] == "executed"

answer = result["answer"]

assert len(answer) == 1

assert answer.iloc[0]["category"] == "Office"

assert answer.iloc[0]["average"] == 10000.0

print("TEST 3 PASSED")


# -----------------------------------
# TEST 4 — INVALID SORT
# -----------------------------------

print("\nTEST 4 — INVALID SORT")

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
    "group_by": "category",
    "sort": "random"
}

result = execute_plan(
    plan,
    tables
)

print(result)

assert result["status"] == "execution_error"

assert (
    result["reason"]
    == "Sort must be either 'ascending' or 'descending'."
)

print("TEST 4 PASSED")


# -----------------------------------
# TEST 5 — INVALID LIMIT
# -----------------------------------

print("\nTEST 5 — INVALID LIMIT")

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
    "group_by": "category",
    "sort": "descending",
    "limit": 0
}

result = execute_plan(
    plan,
    tables
)

print(result)

assert result["status"] == "execution_error"

assert (
    result["reason"]
    == "TOP N value must be greater than zero."
)

print("TEST 5 PASSED")


# -----------------------------------
# FINAL RESULT
# -----------------------------------

print("\n===================================")
print("ALL EXECUTOR SORT + TOP N TESTS PASSED")
print("===================================")