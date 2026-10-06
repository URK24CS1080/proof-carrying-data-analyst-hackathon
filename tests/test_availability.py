from src.data.loader import load_table
from src.data.profiler import check_date_availability


# Load sales data
df = load_table("test_data/sales.csv")


print("DATE AVAILABILITY")
print("-----------------")

# Date inside the available range
result = check_date_availability(
    df,
    "date",
    "2026-01-15"
)

print("\nRequest: 2026-01-15")
print(result)


# Date outside the available range
result = check_date_availability(
    df,
    "date",
    "2027-03-01"
)

print("\nRequest: 2027-03-01")
print(result)


# Invalid date
result = check_date_availability(
    df,
    "date",
    "not-a-date"
)

print("\nRequest: not-a-date")
print(result)