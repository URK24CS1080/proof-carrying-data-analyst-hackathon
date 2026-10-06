from src.data.loader import load_table
from src.data.profiler import profile_table


df = load_table("test_data/sales.csv")

profile = profile_table(df)

print("PROFILE")
print("-------")

print("Rows:", profile["rows"])
print("Columns:", profile["columns"])

print("Column names:")
print(profile["column_names"])

print("Data types:")
for column, data_type in profile["data_types"].items():
    print(f"  {column}: {data_type}")

print()

print("Missing values:")
for column, count in profile["missing_values"].items():
    print(f"  {column}: {count}")

print()

print("Duplicate rows:", profile["duplicate_rows"])

print()

print("Date columns:", profile["date_columns"])

print()

print("Date ranges:")
for column, date_range in profile["date_ranges"].items():
    print(f"  {column}:")
    print(f"    Min: {date_range['min']}")
    print(f"    Max: {date_range['max']}")

print()

print("Sample rows:")
for row in profile["sample_rows"]:
    print(row)

print()

print("Numeric statistics:")
for column, stats in profile["numeric_statistics"].items():
    print(f"  {column}:")
    print(f"    Min: {stats['min']}")
    print(f"    Max: {stats['max']}")
    print(f"    Mean: {stats['mean']}")

print()

print("Warnings:")
for warning in profile["warnings"]:
    print(f"  - {warning}")

print()

print("Categorical values:")
for column, information in profile["categorical_values"].items():
    print(f"  {column}:")
    print(f"    Unique values: {information['unique_values']}")
    print(f"    Counts: {information['counts']}")


print("\nCurrencies:")
for column, currencies in profile["currencies"].items():
    print(f"  {column}: {currencies}")
