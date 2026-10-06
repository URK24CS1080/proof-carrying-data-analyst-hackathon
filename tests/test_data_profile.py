from src.data.schema import build_data_profile


# Build the complete Data -> Agent profile
profile = build_data_profile([
    "test_data/sales.csv",
    "test_data/customers.csv",
    "test_data/orders.csv"
])


print("COMPLETE DATA PROFILE")
print("=====================")

print("\nTABLES")
print("------")

for table in profile["tables"]:

    print(f"\nTable: {table['name']}")
    print(f"Rows: {table['rows']}")

    print("Columns:")

    for column, data_type in table["columns"].items():
        print(f"  {column}: {data_type}")

    print("Missing values:")
    for column, count in table["missing_values"].items():
        print(f"  {column}: {count}")

    print("Duplicate rows:", table["duplicate_rows"])

    print("Currencies:", table["currencies"])

    print("Units:", table["units"])

    print("Warnings:")

    for warning in table["warnings"]:
        print(f"  - {warning}")


print("\nRELATIONSHIPS")
print("-------------")

for relationship in profile["relationships"]:
    print(relationship)