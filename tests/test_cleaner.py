import pandas as pd

from src.data.cleaner import standardize_column_names
from src.data.cleaner import standardize_column_names
from src.data.cleaner import remove_duplicate_rows
from src.data.cleaner import drop_missing_values
from src.data.cleaner import normalize_date_column
from src.data.cleaner import normalize_numeric_column
from src.data.cleaner import create_cleaning_report

df = pd.DataFrame({
    " Product Name ": ["Laptop", "Mouse"],
    " Revenue ": [50000, 1000],
    "Order Date": ["2026-01-10", "2026-01-11"]
})

cleaned_df = standardize_column_names(df)

print("ORIGINAL COLUMNS")
print(df.columns.tolist())

print()

print("CLEANED COLUMNS")
print(cleaned_df.columns.tolist())

from src.data.cleaner import remove_duplicate_rows

print()

deduplicated_df = remove_duplicate_rows(df)

print("BEFORE DUPLICATE REMOVAL")
print("Rows:", len(df))

print()

print("AFTER DUPLICATE REMOVAL")
print("Rows:", len(deduplicated_df))


from src.data.loader import load_table

print()

sales_df = load_table("test_data/sales.csv")

cleaned_sales = remove_duplicate_rows(sales_df)

print("SALES DATA")
print("Before:", len(sales_df))
print("After:", len(cleaned_sales))

print()

cleaned_missing = drop_missing_values(
    sales_df,
    ["revenue"]
)

print("MISSING VALUE HANDLING")
print("Before:", len(sales_df))
print("After:", len(cleaned_missing))

print()

normalized_sales = normalize_date_column(
    sales_df,
    "date"
)

print("DATE NORMALIZATION")
print("Original type:", sales_df["date"].dtype)
print("Normalized type:", normalized_sales["date"].dtype)

print()

messy_df = pd.DataFrame({
    "revenue": ["50,000", "1,000", "unknown", " 2000 "]
})

normalized_df = normalize_numeric_column(
    messy_df,
    "revenue"
)

print("NUMERIC NORMALIZATION")
print("Original:")
print(messy_df)

print()

print("Normalized:")
print(normalized_df)
print("Type:", normalized_df["revenue"].dtype)

print()

report = create_cleaning_report(
    sales_df,
    cleaned_sales
)

print("CLEANING REPORT")
print("Original rows:", report["original_rows"])
print("Cleaned rows:", report["cleaned_rows"])
print("Rows removed:", report["rows_removed"])
print("Original columns:", report["original_columns"])
print("Cleaned columns:", report["cleaned_columns"])