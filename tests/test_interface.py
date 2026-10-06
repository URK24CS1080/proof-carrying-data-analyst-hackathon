from src.data.schema import build_data_profile
from src.data.interface import create_agent_data_contract


# -----------------------------------------
# Build the complete data profile
# -----------------------------------------
profile = build_data_profile([
    "test_data/sales.csv",
    "test_data/customers.csv",
    "test_data/orders.csv"
])


# -----------------------------------------
# Create Data → Agent contract
# -----------------------------------------
contract = create_agent_data_contract(profile)


# -----------------------------------------
# Display contract
# -----------------------------------------
print("DATA → AGENT CONTRACT")
print("=====================")

print("\nTABLES")
print("------")

for table in contract["tables"]:

    print(f"\nTable: {table['name']}")
    print("Rows:", table["rows"])

    print("Columns:")
    for column, data_type in table["columns"].items():
        print(f"  {column}: {data_type}")

    print("Missing values:")
    for column, count in table["missing_values"].items():
        print(f"  {column}: {count}")

    print("Duplicate rows:", table["duplicate_rows"])

    print("Warnings:")
    for warning in table["warnings"]:
        print("  -", warning)


print("\nRELATIONSHIPS")
print("-------------")

for relationship in contract["relationships"]:
    print(relationship)