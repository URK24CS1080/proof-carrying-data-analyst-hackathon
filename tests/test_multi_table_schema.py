from src.data.loader import load_tables
from src.data.schema import build_multi_table_profile


# Load multiple tables
tables = load_tables([
    "test_data/sales.csv",
    "test_data/customers.csv",
    "test_data/orders.csv"
])


# Build complete profiles
profiles = build_multi_table_profile(tables)


print("MULTI-TABLE PROFILE")
print("-------------------")

for table in profiles["tables"]:

    print(f"\nTable: {table['name']}")
    print(f"Rows: {table['rows']}")

    print("Schema:")

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

print("\nPOSSIBLE RELATIONSHIPS")
print("----------------------")

for relationship in profiles["relationships"]:
    print(relationship)