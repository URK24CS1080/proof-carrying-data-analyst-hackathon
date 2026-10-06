import pandas as pd

from src.executor.operations import sort_values, top_n


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
print("TOP N VALIDATION TESTS")
print("===================================")


# -----------------------------------
# TEST 1 — TOP 1
# -----------------------------------

print("\nTEST 1 — TOP 1")

sorted_sales = sort_values(
    sales,
    column="revenue",
    descending=True
)

result = top_n(
    sorted_sales,
    1
)

print(result)

assert len(result) == 1
assert result.iloc[0]["category"] == "Electronics"
assert result.iloc[0]["revenue"] == 60000

print("TEST 1 PASSED")


# -----------------------------------
# TEST 2 — TOP 2
# -----------------------------------

print("\nTEST 2 — TOP 2")

result = top_n(
    sorted_sales,
    2
)

print(result)

assert len(result) == 2
assert result["category"].tolist() == [
    "Electronics",
    "Furniture"
]

assert result["revenue"].tolist() == [
    60000,
    30000
]

print("TEST 2 PASSED")


# -----------------------------------
# TEST 3 — N Greater Than Rows
# -----------------------------------

print("\nTEST 3 — TOP N Greater Than Row Count")

result = top_n(
    sorted_sales,
    10
)

print(result)

assert len(result) == 4

print("TEST 3 PASSED")


# -----------------------------------
# TEST 4 — N = 0
# -----------------------------------

print("\nTEST 4 — TOP 0")

try:

    top_n(
        sorted_sales,
        0
    )

    assert False, "Expected ValueError"

except ValueError as exc:

    print(exc)

    assert "TOP N value must be greater than zero." in str(exc)

print("TEST 4 PASSED")


# -----------------------------------
# TEST 5 — Negative N
# -----------------------------------

print("\nTEST 5 — Negative TOP N")

try:

    top_n(
        sorted_sales,
        -1
    )

    assert False, "Expected ValueError"

except ValueError as exc:

    print(exc)

    assert "TOP N value must be greater than zero." in str(exc)

print("TEST 5 PASSED")


# -----------------------------------
# TEST 6 — Non-Integer N
# -----------------------------------

print("\nTEST 6 — Non-Integer TOP N")

try:

    top_n(
        sorted_sales,
        1.5
    )

    assert False, "Expected ValueError"

except ValueError as exc:

    print(exc)

    assert "TOP N value must be an integer." in str(exc)

print("TEST 6 PASSED")


# -----------------------------------
# TEST 7 — Empty DataFrame
# -----------------------------------

print("\nTEST 7 — Empty DataFrame")

empty_df = pd.DataFrame({
    "category": [],
    "revenue": []
})

try:

    top_n(
        empty_df,
        1
    )

    assert False, "Expected ValueError"

except ValueError as exc:

    print(exc)

    assert "Cannot select TOP N from an empty DataFrame." in str(exc)

print("TEST 7 PASSED")


# -----------------------------------
# FINAL RESULT
# -----------------------------------

print("\n===================================")
print("ALL TOP N VALIDATION TESTS PASSED")
print("===================================")