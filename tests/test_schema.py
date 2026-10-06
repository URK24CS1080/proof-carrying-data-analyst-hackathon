from src.data.loader import load_table
from src.data.schema import build_table_profile


# Load one table
df = load_table("test_data/sales.csv")


# Build complete profile
profile = build_table_profile(
    df,
    "sales"
)


print("COMPLETE TABLE PROFILE")
print("----------------------")

print("Name:", profile["name"])
print("Rows:", profile["rows"])

print("\nSchema:")
for column, data_type in profile["columns"].items():
    print(f"  {column}: {data_type}")

print("\nMissing values:")
for column, count in profile["missing_values"].items():
    print(f"  {column}: {count}")

print("\nDuplicate rows:")
print(profile["duplicate_rows"])

print("\nDate columns:")
print(profile["date_columns"])

print("\nCurrencies:")
print(profile["currencies"])

print("\nUnits:")
print(profile["units"])

print("\nWarnings:")
for warning in profile["warnings"]:
    print(f"  - {warning}")