import pandas as pd

from src.executor.pipeline import run_verified_analysis


print("===================================")
print("EVIDENCE TESTS")
print("===================================")


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
# TEST 1 — BASIC EVIDENCE
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
}

result = run_verified_analysis(
    plan,
    tables,
)

print("\nTEST 1 — BASIC EVIDENCE")
print(result["evidence"])

assert result["status"] == "verified"

assert result["evidence"]["tables"] == [
    "sales"
]

assert result["evidence"]["rows_analyzed"] == 4

assert result["evidence"]["columns"] == [
    "revenue"
]

assert result["evidence"]["filters"] == {}

assert result["evidence"]["operation"] == "average"

print("TEST 1 PASSED")


# --------------------------------------------------
# TEST 2 — FILTER EVIDENCE
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

print("\nTEST 2 — FILTER EVIDENCE")
print(result["evidence"])

assert result["status"] == "verified"

assert result["evidence"]["tables"] == [
    "sales"
]

assert result["evidence"]["rows_analyzed"] == 3

assert "revenue" in result["evidence"]["columns"]

assert "category" in result["evidence"]["columns"]

assert result["evidence"]["filters"] == {
    "category": "Electronics"
}

assert result["evidence"]["operation"] == "average"

print("TEST 2 PASSED")


# --------------------------------------------------
# TEST 3 — GROUP BY EVIDENCE
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
    "group_by": "category",
}

result = run_verified_analysis(
    plan,
    tables,
)

print("\nTEST 3 — GROUP BY EVIDENCE")
print(result["evidence"])

assert result["status"] == "verified"

assert result["evidence"]["tables"] == [
    "sales"
]

assert result["evidence"]["rows_analyzed"] == 4

assert "revenue" in result["evidence"]["columns"]

assert "category" in result["evidence"]["columns"]

assert result["evidence"]["operation"] == "group_average"

print("TEST 3 PASSED")


# --------------------------------------------------
# TEST 4 — JOIN EVIDENCE
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "product_name": "Laptop"
    },
    "join": {
        "table": "products",
        "left_on": "product_id",
        "right_on": "product_id"
    },
}

result = run_verified_analysis(
    plan,
    tables,
)

print("\nTEST 4 — JOIN EVIDENCE")
print(result["evidence"])

assert result["status"] == "verified"

assert result["evidence"]["tables"] == [
    "sales",
    "products"
]

assert result["evidence"]["rows_analyzed"] == 1

assert "revenue" in result["evidence"]["columns"]

assert "product_name" in result["evidence"]["columns"]

assert "product_id" in result["evidence"]["columns"]

assert result["evidence"]["filters"] == {
    "product_name": "Laptop"
}

assert result["evidence"]["operation"] == "average"

assert result["evidence"]["join"]["table"] == "products"

assert result["evidence"]["join"]["left_on"] == "product_id"

assert result["evidence"]["join"]["right_on"] == "product_id"

print("TEST 4 PASSED")


# --------------------------------------------------
# TEST 5 — DATE FILTER EVIDENCE
# --------------------------------------------------

sales_with_dates = sales.copy()

sales_with_dates["date"] = [
    "2025-01-10",
    "2025-02-10",
    "2026-01-10",
    "2026-02-10",
]

tables_with_dates = {
    "sales": sales_with_dates,
}

plan = {
    "status": "answerable",
    "operation": "sum",
    "table": "sales",
    "column": "revenue",
    "date_filter": {
        "column": "date",
        "start": "2025-01-01",
        "end": "2025-12-31"
    },
}

result = run_verified_analysis(
    plan,
    tables_with_dates,
)

print("\nTEST 5 — DATE FILTER EVIDENCE")
print(result["evidence"])

assert result["status"] == "verified"

assert result["evidence"]["rows_analyzed"] == 2

assert "date" in result["evidence"]["columns"]

assert result["evidence"]["date_filter"] == {
    "column": "date",
    "start": "2025-01-01",
    "end": "2025-12-31"
}

print("TEST 5 PASSED")


print("\n===================================")
print("ALL EVIDENCE TESTS PASSED")
print("===================================")