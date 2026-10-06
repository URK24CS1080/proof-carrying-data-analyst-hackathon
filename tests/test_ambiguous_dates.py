from src.data.loader import load_table
from src.data.schema import build_table_profile


# Load ambiguous-date dataset
df = load_table("test_data/ambiguous_dates.csv")


# Build complete profile
profile = build_table_profile(
    df,
    "ambiguous_dates"
)


print("AMBIGUOUS DATE PROFILE")
print("-----------------------")

print("Rows:", profile["rows"])

print("\nSchema:")
for column, data_type in profile["columns"].items():
    print(f"  {column}: {data_type}")

print("\nDate columns:")
print(profile["date_columns"])

print("\nDate ranges:")
for column, date_range in profile["date_ranges"].items():
    print(f"  {column}:")
    print(f"    Min: {date_range['min']}")
    print(f"    Max: {date_range['max']}")

print("\nWarnings:")
for warning in profile["warnings"]:
    print(f"  - {warning}")