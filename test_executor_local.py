import pandas as pd

from src.executor.executor import execute_plan


# --------------------------------------------------
# Test data
# --------------------------------------------------

sales = pd.DataFrame({
    "product": ["Laptop", "Phone", "Tablet", "Monitor"],
    "category": [
        "Electronics",
        "Electronics",
        "Electronics",
        "Office"
    ],
    "revenue": [60000, 30000, 20000, 10000],
    "product_name": ["A", "B", "C", "D"],
})


missing_data = pd.DataFrame({
    "revenue": [None, None, None]
})


tables = {
    "sales": sales,
    "missing_data": missing_data
}


# ==================================================
# TEST 1 — Valid average
# ==================================================

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue"
}

result = execute_plan(plan, tables)

print("\nTEST 1 — Valid Average")
print(result)

assert result["status"] == "executed"
assert result["answer"] == 30000.0


# ==================================================
# TEST 2 — Table does not exist
# ==================================================

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "unknown_table",
    "column": "revenue"
}

result = execute_plan(plan, tables)

print("\nTEST 2 — Missing Table")
print(result)

assert result["status"] == "execution_error"
assert result["answer"] is None


# ==================================================
# TEST 3 — Column does not exist
# ==================================================

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "profit"
}

result = execute_plan(plan, tables)

print("\nTEST 3 — Missing Column")
print(result)

assert result["status"] == "execution_error"
assert result["answer"] is None


# ==================================================
# TEST 4 — Column is not numeric
# ==================================================

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "product_name"
}

result = execute_plan(plan, tables)

print("\nTEST 4 — Non-Numeric Column")
print(result)

assert result["status"] == "execution_error"
assert result["answer"] is None


# ==================================================
# TEST 5 — Column contains no valid values
# ==================================================

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "missing_data",
    "column": "revenue"
}

result = execute_plan(plan, tables)

print("\nTEST 5 — No Valid Values")
print(result)

assert result["status"] == "execution_error"
assert result["answer"] is None


# ==================================================
# TEST 6 — Unsupported operation
# ==================================================

plan = {
    "status": "answerable",
    "operation": "median",
    "table": "sales",
    "column": "revenue"
}

result = execute_plan(plan, tables)

print("\nTEST 6 — Unsupported Operation")
print(result)

assert result["status"] == "execution_error"
assert result["answer"] is None


# ==================================================
# TEST 7 — Plan says cannot determine
# ==================================================

plan = {
    "status": "cannot_determine",
    "reason": "The requested year does not exist in the data."
}

result = execute_plan(plan, tables)

print("\nTEST 7 — Cannot Determine")
print(result)

assert result["status"] == "cannot_determine"
assert result["answer"] is None


print("\n===================================")
print("ALL STEP 5 TESTS PASSED")
print("===================================")


# ==================================================
# TEST 1B — Average with filter
# ==================================================

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "category": "Electronics"
    }
}

result = execute_plan(plan, tables)

print("\nTEST 1B — Average With Filter")
print(result)

assert result["status"] == "executed"
assert result["answer"] == 36666.666666666664
assert result["rows_analyzed"] == 3


# ==================================================
# TEST 1C — Invalid filter column
# ==================================================

plan = {
    "status": "answerable",
    "operation": "average",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "department": "Electronics"
    }
}

result = execute_plan(plan, tables)

print("\nTEST 1C — Invalid Filter Column")
print(result)

assert result["status"] == "execution_error"
assert result["answer"] is None


# ==================================================
# TEST 8 — Count
# ==================================================

plan = {
    "status": "answerable",
    "operation": "count",
    "table": "sales",
    "column": "product",
}

result = execute_plan(plan, tables)

print("\nTEST 8 — Count")
print(result)

assert result["status"] == "executed"
assert result["answer"] == 4
assert result["rows_analyzed"] == 4


# ==================================================
# TEST 9 — Count With Filter
# ==================================================

plan = {
    "status": "answerable",
    "operation": "count",
    "table": "sales",
    "column": "product",
    "filters": {
        "category": "Electronics"
    }
}

result = execute_plan(plan, tables)

print("\nTEST 9 — Count With Filter")
print(result)

assert result["status"] == "executed"
assert result["answer"] == 3
assert result["rows_analyzed"] == 3


print("\n===================================")
print("ALL COUNT TESTS PASSED")
print("===================================")


# ==================================================
# TEST 10 — Sum
# ==================================================

plan = {
    "status": "answerable",
    "operation": "sum",
    "table": "sales",
    "column": "revenue",
}

result = execute_plan(plan, tables)

print("\nTEST 10 — Sum")
print(result)

assert result["status"] == "executed"
assert result["answer"] == 120000.0
assert result["rows_analyzed"] == 4


# ==================================================
# TEST 11 — Sum With Filter
# ==================================================

plan = {
    "status": "answerable",
    "operation": "sum",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "category": "Electronics"
    }
}

result = execute_plan(plan, tables)

print("\nTEST 11 — Sum With Filter")
print(result)

assert result["status"] == "executed"
assert result["answer"] == 110000.0
assert result["rows_analyzed"] == 3


# ==================================================
# TEST 12 — Sum Missing Column
# ==================================================

plan = {
    "status": "answerable",
    "operation": "sum",
    "table": "sales",
    "column": "profit",
}

result = execute_plan(plan, tables)

print("\nTEST 12 — Sum Missing Column")
print(result)

assert result["status"] == "execution_error"
assert result["answer"] is None


# ==================================================
# TEST 13 — Sum Non-Numeric Column
# ==================================================

plan = {
    "status": "answerable",
    "operation": "sum",
    "table": "sales",
    "column": "product_name",
}

result = execute_plan(plan, tables)

print("\nTEST 13 — Sum Non-Numeric Column")
print(result)

assert result["status"] == "execution_error"
assert result["answer"] is None


print("\n===================================")
print("ALL SUM TESTS PASSED")
print("===================================")


# ==================================================
# TEST 14 — Minimum
# ==================================================

plan = {
    "status": "answerable",
    "operation": "min",
    "table": "sales",
    "column": "revenue",
}

result = execute_plan(plan, tables)

print("\nTEST 14 — Minimum")
print(result)

assert result["status"] == "executed"
assert result["answer"] == 10000.0
assert result["rows_analyzed"] == 4


# ==================================================
# TEST 15 — Maximum
# ==================================================

plan = {
    "status": "answerable",
    "operation": "max",
    "table": "sales",
    "column": "revenue",
}

result = execute_plan(plan, tables)

print("\nTEST 15 — Maximum")
print(result)

assert result["status"] == "executed"
assert result["answer"] == 60000.0
assert result["rows_analyzed"] == 4


# ==================================================
# TEST 16 — Minimum With Filter
# ==================================================

plan = {
    "status": "answerable",
    "operation": "min",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "category": "Electronics"
    }
}

result = execute_plan(plan, tables)

print("\nTEST 16 — Minimum With Filter")
print(result)

assert result["status"] == "executed"
assert result["answer"] == 20000.0
assert result["rows_analyzed"] == 3


# ==================================================
# TEST 17 — Maximum With Filter
# ==================================================

plan = {
    "status": "answerable",
    "operation": "max",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "category": "Electronics"
    }
}

result = execute_plan(plan, tables)

print("\nTEST 17 — Maximum With Filter")
print(result)

assert result["status"] == "executed"
assert result["answer"] == 60000.0
assert result["rows_analyzed"] == 3


print("\n===================================")
print("ALL MIN/MAX TESTS PASSED")
print("===================================")


# ==================================================
# DATE FILTER TEST DATA
# ==================================================

date_sales = pd.DataFrame({
    "product": [
        "Laptop",
        "Phone",
        "Tablet",
        "Monitor",
        "Keyboard"
    ],
    "category": [
        "Electronics",
        "Electronics",
        "Electronics",
        "Office",
        "Office"
    ],
    "revenue": [
        60000,
        30000,
        20000,
        10000,
        5000
    ],
    "date": [
        "2025-01-15",
        "2025-03-20",
        "2025-06-10",
        "2026-01-10",
        "2026-03-15"
    ],
})

date_tables = {
    "sales": date_sales
}


# ==================================================
# TEST 18 — Date Filter
# ==================================================

plan = {
    "status": "answerable",
    "operation": "sum",
    "table": "sales",
    "column": "revenue",
    "date_filter": {
        "column": "date",
        "start": "2025-01-01",
        "end": "2025-12-31"
    }
}

result = execute_plan(plan, date_tables)

print("\nTEST 18 — Date Filter")
print(result)

assert result["status"] == "executed"
assert result["answer"] == 110000.0
assert result["rows_analyzed"] == 3


# ==================================================
# TEST 19 — Date Filter With Category Filter
# ==================================================

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
        "end": "2025-12-31"
    }
}

result = execute_plan(plan, date_tables)

print("\nTEST 19 — Date Filter + Normal Filter")
print(result)

assert result["status"] == "executed"
assert result["answer"] == 36666.666666666664
assert result["rows_analyzed"] == 3


# ==================================================
# TEST 20 — Invalid Date Column
# ==================================================

plan = {
    "status": "answerable",
    "operation": "sum",
    "table": "sales",
    "column": "revenue",
    "date_filter": {
        "column": "transaction_date",
        "start": "2025-01-01",
        "end": "2025-12-31"
    }
}

result = execute_plan(plan, date_tables)

print("\nTEST 20 — Invalid Date Column")
print(result)

assert result["status"] == "execution_error"
assert result["answer"] is None


# ==================================================
# TEST 21 — Date Range With No Records
# ==================================================

plan = {
    "status": "answerable",
    "operation": "sum",
    "table": "sales",
    "column": "revenue",
    "date_filter": {
        "column": "date",
        "start": "2027-01-01",
        "end": "2027-12-31"
    }
}

result = execute_plan(plan, date_tables)

print("\nTEST 21 — Date Range With No Records")
print(result)

assert result["status"] == "cannot_determine"
assert result["answer"] is None
assert result["rows_analyzed"] == 0


print("\n===================================")
print("ALL DATE FILTER TESTS PASSED")
print("===================================")


# --------------------------------------------------
# TEST 22 — Normal Filter With No Records
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "sum",
    "table": "sales",
    "column": "revenue",
    "filters": {
        "category": "NonExistingCategory"
    }
}

result = execute_plan(
    plan,
    tables
)

print("\nTEST 22 — Normal Filter With No Records")
print(result)

assert result["status"] == "cannot_determine"
assert result["answer"] is None
assert result["reason"] == "The applied filters matched no rows."
assert result["rows_analyzed"] == 0


# --------------------------------------------------
# TEST 23 — Group Average
# --------------------------------------------------

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
    "group_by": "category",
}

result = execute_plan(
    plan,
    tables
)

print("\nTEST 23 — Group Average")
print(result)

assert result["status"] == "executed"
assert result["operation"] == "group_average"
assert result["group_by"] == "category"
assert len(result["answer"]) == 2

electronics_average = result["answer"].loc[
    result["answer"]["category"] == "Electronics",
    "average"
].iloc[0]

office_average = result["answer"].loc[
    result["answer"]["category"] == "Office",
    "average"
].iloc[0]

assert electronics_average == 36666.666666666664
assert office_average == 10000.0


print("\n===================================")
print("GROUP AVERAGE TEST PASSED")
print("===================================")


# ============================================================
# GROUP BY VALIDATION TESTS
# ============================================================


# ============================================================
# TEST 24 — GROUP BY With Missing Group Column
# ============================================================

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
    "group_by": "department",
}

result = execute_plan(
    plan,
    tables
)

print("\nTEST 24 — Group Average With Missing Group Column")
print(result)

assert result["status"] == "execution_error"
assert result["answer"] is None
assert result["reason"] == "Group-by column 'department' does not exist."


# ============================================================
# TEST 25 — GROUP BY With Missing Aggregation Column
# ============================================================

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "profit",
    "group_by": "category",
}

result = execute_plan(
    plan,
    tables
)

print("\nTEST 25 — Group Average With Missing Aggregation Column")
print(result)

assert result["status"] == "execution_error"
assert result["answer"] is None
assert result["reason"] == "Column 'profit' does not exist."


# ============================================================
# TEST 26 — GROUP BY With Non-Numeric Aggregation Column
# ============================================================

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "product_name",
    "group_by": "category",
}

result = execute_plan(
    plan,
    tables
)

print("\nTEST 26 — Group Average With Non-Numeric Column")
print(result)

assert result["status"] == "execution_error"
assert result["answer"] is None
assert result["reason"] == (
    "Column 'product_name' must contain numeric values."
)


# ============================================================
# TEST 27 — GROUP BY With Normal Filter
# ============================================================

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
    "group_by": "category",
    "filters": {
        "category": "Electronics"
    },
}

result = execute_plan(
    plan,
    tables
)

print("\nTEST 27 — Group Average With Filter")
print(result)

assert result["status"] == "executed"
assert result["operation"] == "group_average"
assert result["group_by"] == "category"
assert len(result["answer"]) == 1

electronics_average = result["answer"].loc[
    result["answer"]["category"] == "Electronics",
    "average"
].iloc[0]

assert electronics_average == 36666.666666666664


# ============================================================
# TEST 28 — GROUP BY With Date Filter
# ============================================================

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
    "group_by": "category",
    "date_filter": {
        "column": "date",
        "start": "2025-01-01",
        "end": "2025-12-31",
    },
}

# IMPORTANT:
# Use date_tables here because the normal 'tables' dataset
# does not contain a 'date' column.

result = execute_plan(
    plan,
    date_tables
)

print("\nTEST 28 — Group Average With Date Filter")
print(result)

assert result["status"] == "executed"
assert result["operation"] == "group_average"
assert result["group_by"] == "category"

# 2025 contains:
# Electronics -> 60000, 30000, 20000
# Office -> no 2025 records
assert len(result["answer"]) == 1

electronics_average = result["answer"].loc[
    result["answer"]["category"] == "Electronics",
    "average"
].iloc[0]

assert electronics_average == 36666.666666666664


# ============================================================
# TEST 29 — GROUP BY With Zero Matching Rows
# ============================================================

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
    "group_by": "category",
    "filters": {
        "category": "NonExistingCategory"
    },
}

result = execute_plan(
    plan,
    tables
)

print("\nTEST 29 — Group Average With No Matching Rows")
print(result)

assert result["status"] == "cannot_determine"
assert result["answer"] is None
assert result["reason"] == "The applied filters matched no rows."
assert result["rows_analyzed"] == 0


# ============================================================
# TEST 30 — GROUP BY Without group_by Field
# ============================================================

plan = {
    "status": "answerable",
    "operation": "group_average",
    "table": "sales",
    "column": "revenue",
}

result = execute_plan(
    plan,
    tables
)

print("\nTEST 30 — Group Average Without Group Column")
print(result)

assert result["status"] == "execution_error"
assert result["answer"] is None
assert result["reason"] == (
    "GROUP BY operation requires a 'group_by' column."
)


print("\n===================================")
print("ALL GROUP BY VALIDATION TESTS PASSED")
print("===================================")