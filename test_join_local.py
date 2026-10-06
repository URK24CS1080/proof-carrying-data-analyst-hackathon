import pandas as pd

from src.executor.operations import join_tables


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
print("JOIN VALIDATION TESTS")
print("===================================")


# -----------------------------------
# TEST 1 — INNER JOIN
# -----------------------------------

print("\nTEST 1 — INNER JOIN")

result = join_tables(
    left_df=sales,
    right_df=products,
    left_on="product_id",
    right_on="product_id"
)

print(result)

assert len(result) == 3

assert result["product_id"].tolist() == [
    "P1",
    "P2",
    "P3"
]

print("TEST 1 PASSED")


# -----------------------------------
# TEST 2 — VERIFY VALUES
# -----------------------------------

print("\nTEST 2 — VERIFY JOINED VALUES")

assert result.iloc[0]["revenue"] == 60000
assert result.iloc[0]["category"] == "Electronics"

assert result.iloc[1]["revenue"] == 30000
assert result.iloc[1]["category"] == "Electronics"

assert result.iloc[2]["revenue"] == 20000
assert result.iloc[2]["category"] == "Office"

print("TEST 2 PASSED")


# -----------------------------------
# TEST 3 — INVALID LEFT COLUMN
# -----------------------------------

print("\nTEST 3 — INVALID LEFT JOIN COLUMN")

try:

    join_tables(
        left_df=sales,
        right_df=products,
        left_on="customer_id",
        right_on="product_id"
    )

    assert False, "Expected ValueError"

except ValueError as exc:

    print(exc)

    assert (
        "Left join column 'customer_id' does not exist."
        in str(exc)
    )

print("TEST 3 PASSED")


# -----------------------------------
# TEST 4 — INVALID RIGHT COLUMN
# -----------------------------------

print("\nTEST 4 — INVALID RIGHT JOIN COLUMN")

try:

    join_tables(
        left_df=sales,
        right_df=products,
        left_on="product_id",
        right_on="category_id"
    )

    assert False, "Expected ValueError"

except ValueError as exc:

    print(exc)

    assert (
        "Right join column 'category_id' does not exist."
        in str(exc)
    )

print("TEST 4 PASSED")


# -----------------------------------
# TEST 5 — UNSUPPORTED JOIN TYPE
# -----------------------------------

print("\nTEST 5 — UNSUPPORTED JOIN TYPE")

try:

    join_tables(
        left_df=sales,
        right_df=products,
        left_on="product_id",
        right_on="product_id",
        how="left"
    )

    assert False, "Expected ValueError"

except ValueError as exc:

    print(exc)

    assert (
        "Only 'inner' JOIN is supported."
        in str(exc)
    )

print("TEST 5 PASSED")


# -----------------------------------
# TEST 6 — EMPTY LEFT TABLE
# -----------------------------------

print("\nTEST 6 — EMPTY LEFT TABLE")

empty_sales = pd.DataFrame({
    "product_id": [],
    "revenue": []
})

try:

    join_tables(
        left_df=empty_sales,
        right_df=products,
        left_on="product_id",
        right_on="product_id"
    )

    assert False, "Expected ValueError"

except ValueError as exc:

    print(exc)

    assert (
        "Cannot join an empty left table."
        in str(exc)
    )

print("TEST 6 PASSED")


# -----------------------------------
# TEST 7 — EMPTY RIGHT TABLE
# -----------------------------------

print("\nTEST 7 — EMPTY RIGHT TABLE")

empty_products = pd.DataFrame({
    "product_id": [],
    "category": []
})

try:

    join_tables(
        left_df=sales,
        right_df=empty_products,
        left_on="product_id",
        right_on="product_id"
    )

    assert False, "Expected ValueError"

except ValueError as exc:

    print(exc)

    assert (
        "Cannot join an empty right table."
        in str(exc)
    )

print("TEST 7 PASSED")


# -----------------------------------
# FINAL RESULT
# -----------------------------------

print("\n===================================")
print("ALL JOIN VALIDATION TESTS PASSED")
print("===================================")