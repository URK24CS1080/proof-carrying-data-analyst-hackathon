import pandas as pd

from src.data.contradiction import find_contradictions


# -----------------------------------------
# Table 1
# -----------------------------------------
customers_a = pd.DataFrame({
    "customer_id": [1, 2, 3],
    "city": [
        "Chennai",
        "Coimbatore",
        "Bangalore"
    ]
})


# -----------------------------------------
# Table 2
# -----------------------------------------
customers_b = pd.DataFrame({
    "customer_id": [1, 2, 3],
    "city": [
        "Chennai",
        "Chennai",
        "Bangalore"
    ]
})


# -----------------------------------------
# Find contradictions
# -----------------------------------------
contradictions = find_contradictions(
    customers_a,
    customers_b,
    key_column_a="customer_id",
    key_column_b="customer_id",
    value_column_a="city",
    value_column_b="city"
)


# -----------------------------------------
# Display result
# -----------------------------------------
print("CONTRADICTION DETECTION")
print("=======================")

for contradiction in contradictions:
    print(contradiction)