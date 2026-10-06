from src.data.loader import load_tables


tables = load_tables([
    "test_data/sales.csv",
    "test_data/customers.csv"
])

print("TABLES LOADED")
print("-------------")

for table_name, df in tables.items():
    print(f"Table: {table_name}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print()