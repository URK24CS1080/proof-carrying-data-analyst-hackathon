import pandas as pd


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize DataFrame column names.

    - Removes leading/trailing spaces
    - Converts names to lowercase
    - Replaces spaces with underscores

    The original DataFrame is not modified.
    """

    cleaned_df = df.copy()

    cleaned_df.columns = [
        str(column).strip().lower().replace(" ", "_")
        for column in cleaned_df.columns
    ]

    return cleaned_df

def remove_duplicate_rows(
    df: pd.DataFrame,
    keep: str = "first"
) -> pd.DataFrame:
    """
    Remove duplicate rows from a DataFrame.

    The original DataFrame is not modified.

    keep:
        "first" - keep the first occurrence
        "last"  - keep the last occurrence
        False    - remove all duplicate occurrences
    """

    cleaned_df = df.copy()

    cleaned_df = cleaned_df.drop_duplicates(
        keep=keep
    )

    return cleaned_df

def drop_missing_values(
    df: pd.DataFrame,
    columns: list[str]
) -> pd.DataFrame:
    """
    Remove rows where selected columns contain missing values.

    The original DataFrame is not modified.
    """

    cleaned_df = df.copy()

    cleaned_df = cleaned_df.dropna(
        subset=columns
    )

    return cleaned_df

def normalize_date_column(
    df: pd.DataFrame,
    column: str
) -> pd.DataFrame:
    """
    Convert a selected column to Pandas datetime.

    Invalid date values become NaT instead of causing an error.

    The original DataFrame is not modified.
    """

    cleaned_df = df.copy()

    cleaned_df[column] = pd.to_datetime(
        cleaned_df[column],
        errors="coerce",
        format="mixed"
    )

    return cleaned_df

def normalize_numeric_column(
    df: pd.DataFrame,
    column: str
) -> pd.DataFrame:
    """
    Convert a selected column to numeric values.

    Commas and surrounding spaces are removed before conversion.
    Invalid values become NaN.

    The original DataFrame is not modified.
    """

    cleaned_df = df.copy()

    cleaned_df[column] = (
        cleaned_df[column]
        .astype("string")
        .str.strip()
        .str.replace(",", "", regex=False)
    )

    cleaned_df[column] = pd.to_numeric(
        cleaned_df[column],
        errors="coerce"
    )

    return cleaned_df

def create_cleaning_report(
    original_df: pd.DataFrame,
    cleaned_df: pd.DataFrame
) -> dict:
    """
    Create a basic report describing changes between
    the original and cleaned DataFrames.

    This function does not modify either DataFrame.
    """

    report = {
        "original_rows": len(original_df),
        "cleaned_rows": len(cleaned_df),
        "rows_removed": len(original_df) - len(cleaned_df),
        "original_columns": list(original_df.columns),
        "cleaned_columns": list(cleaned_df.columns)
    }

    return report