from src.data.loader import load_tables
from src.data.profiler import profile_tables


tables = load_tables([
    "test_data/sales.csv",
    "test_data/customers.csv"
])

profiles = profile_tables(tables)

print("MULTI-TABLE PROFILES")
print("--------------------")

for table_name, profile in profiles.items():
    print()
    print("Table:", table_name)
    print("Rows:", profile["rows"])
    print("Columns:", profile["column_names"])
    print("Date columns:", profile["date_columns"])
    print("Duplicate rows:", profile["duplicate_rows"])