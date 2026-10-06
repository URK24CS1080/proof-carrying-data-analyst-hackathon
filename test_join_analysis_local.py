import pandas as pd

from src.executor.operations import (
    join_tables,
    apply_filters,
    average,
)


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


print("===================================")
print("JOIN + FILTER + AVERAGE TEST")
print("===================================")


# -----------------------------------
# STEP 1 — JOIN
# -----------------------------------

print("\nSTEP 1 — INNER JOIN")

joined = join_tables(
    left_df=sales,
    right_df=products,
    left_on="product_id",
    right_on="product_id"
)

print(joined)

assert len(joined) == 3

print("JOIN PASSED")


# -----------------------------------
# STEP 2 — FILTER
# -----------------------------------

print("\nSTEP 2 — FILTER ELECTRONICS")

filtered = apply_filters(
    joined,
    {
        "category": "Electronics"
    }
)

print(filtered)

assert len(filtered) == 2

assert filtered["product_id"].tolist() == [
    "P1",
    "P2"
]

print("FILTER PASSED")


# -----------------------------------
# STEP 3 — AVERAGE
# -----------------------------------

print("\nSTEP 3 — AVERAGE REVENUE")

result = average(
    filtered,
    "revenue"
)

print("Average revenue:", result)

assert result == 45000.0

print("AVERAGE PASSED")


# -----------------------------------
# FINAL RESULT
# -----------------------------------

print("\n===================================")
print("FINAL RESULT")
print("===================================")

print(
    f"Average Electronics revenue: {result:.2f}"
)

print("\n===================================")
print("JOIN + FILTER + AVERAGE TEST PASSED")
print("===================================")