import pandas as pd

from src.executor.operations import (
    group_average,
    sort_values,
    top_n,
)


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


print("===================================")
print("GROUP + SORT + TOP N TEST")
print("===================================")


# -----------------------------------
# STEP 1 — GROUP AVERAGE
# -----------------------------------

print("\nSTEP 1 — GROUP AVERAGE")

grouped = group_average(
    df=sales,
    column="revenue",
    group_by="category"
)

print(grouped)

assert len(grouped) == 4

print("GROUP AVERAGE PASSED")


# -----------------------------------
# STEP 2 — SORT DESCENDING
# -----------------------------------

print("\nSTEP 2 — SORT DESCENDING")

sorted_result = sort_values(
    grouped,
    column="average",
    descending=True
)

print(sorted_result)

assert sorted_result.iloc[0]["category"] == "Electronics"

assert sorted_result.iloc[0]["average"] == (
    110000 / 3
)

print("SORT PASSED")


# -----------------------------------
# STEP 3 — TOP 1
# -----------------------------------

print("\nSTEP 3 — TOP 1")

result = top_n(
    sorted_result,
    1
)

print(result)

assert len(result) == 1

assert result.iloc[0]["category"] == "Electronics"

assert abs(
    result.iloc[0]["average"] - 36666.666666666664
) < 0.000001

print("TOP 1 PASSED")


# -----------------------------------
# FINAL ANSWER
# -----------------------------------

category = result.iloc[0]["category"]
average_revenue = result.iloc[0]["average"]


print("\n===================================")
print("FINAL RESULT")
print("===================================")

print(
    f"Highest average revenue category: {category}"
)

print(
    f"Average revenue: {average_revenue:.2f}"
)


print("\n===================================")
print("GROUP + SORT + TOP N TEST PASSED")
print("===================================")