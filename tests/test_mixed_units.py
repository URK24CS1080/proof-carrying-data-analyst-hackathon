from src.data.loader import load_table
from src.data.schema import build_table_profile


# Load mixed-unit dataset
df = load_table("test_data/mixed_units.csv")


# Build complete profile
profile = build_table_profile(
    df,
    "mixed_units"
)


print("MIXED UNIT PROFILE")
print("------------------")

print("Rows:", profile["rows"])

print("\nSchema:")
for column, data_type in profile["columns"].items():
    print(f"  {column}: {data_type}")

print("\nUnits:")
print(profile["units"])

print("\nWarnings:")
for warning in profile["warnings"]:
    print(f"  - {warning}")