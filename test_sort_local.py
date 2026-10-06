import pandas as pd

from src.executor.operations import sort_values


sales = pd.DataFrame({
    "category": [
        "Electronics",
        "Office",
        "Furniture",
        "Clothing"
    ],
    "revenue": [
        60000,
        10000,
        30000,
        20000
    ]
})


print("===================================")
print("SORT VALIDATION TESTS")
print("===================================")


# -----------------------------------
# TEST 1 — Ascending Sort
# -----------------------------------

print("\nTEST 1 — Ascending Sort")

result = sort_values(
    sales,
    column="revenue",
    descending=False
)

print(result)

assert result["revenue"].tolist() == [
    10000,
    20000,
    30000,
    60000
]

print("TEST 1 PASSED")


# -----------------------------------
# TEST 2 — Descending Sort
# -----------------------------------

print("\nTEST 2 — Descending Sort")

result = sort_values(
    sales,
    column="revenue",
    descending=True
)

print(result)

assert result["revenue"].tolist() == [
    60000,
    30000,
    20000,
    10000
]

print("TEST 2 PASSED")


# -----------------------------------
# TEST 3 — Invalid Column
# -----------------------------------

print("\nTEST 3 — Invalid Sort Column")

try:

    sort_values(
        sales,
        column="profit",
        descending=True
    )

    assert False, "Expected ValueError"

except ValueError as exc:

    print(exc)

    assert "Sort column 'profit' does not exist." in str(exc)

print("TEST 3 PASSED")


# -----------------------------------
# TEST 4 — Empty DataFrame
# -----------------------------------

print("\nTEST 4 — Empty DataFrame")

empty_df = pd.DataFrame({
    "revenue": []
})

try:

    sort_values(
        empty_df,
        column="revenue",
        descending=True
    )

    assert False, "Expected ValueError"

except ValueError as exc:

    print(exc)

    assert "Cannot sort an empty DataFrame." in str(exc)

print("TEST 4 PASSED")


# -----------------------------------
# FINAL RESULT
# -----------------------------------

print("\n===================================")
print("ALL SORT VALIDATION TESTS PASSED")
print("===================================")