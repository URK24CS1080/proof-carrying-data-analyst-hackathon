from src.data.loader import load_table
from src.data.schema import build_table_profile


print("ADVERSARIAL DATA PROFILE")
print("========================")

# -----------------------------------------
# Load messy data
# -----------------------------------------
df = load_table("test_data/messy_sales.csv")

# -----------------------------------------
# Build complete profile
# -----------------------------------------
profile = build_table_profile(
    df,
    "messy_sales"
)

# -----------------------------------------
# Display results
# -----------------------------------------
print("\nTABLE")
print("-----")
print("Name:", profile["name"])
print("Rows:", profile["rows"])

print("\nSCHEMA")
print("------")
for column, data_type in profile["columns"].items():
    print(f"  {column}: {data_type}")

print("\nMISSING VALUES")
print("--------------")
for column, count in profile["missing_values"].items():
    print(f"  {column}: {count}")

print("\nDUPLICATES")
print("----------")
print(profile["duplicate_rows"])

print("\nDATES")
print("-----")
print(profile["date_columns"])
print(profile["date_ranges"])

print("\nCURRENCIES")
print("----------")
print(profile["currencies"])

print("\nUNITS")
print("-----")
print(profile["units"])

print("\nWARNINGS")
print("--------")
for warning in profile["warnings"]:
    print(" -", warning)

print("\nSAMPLE ROWS")
print("-----------")
for row in profile["sample_rows"]:
    print(row)