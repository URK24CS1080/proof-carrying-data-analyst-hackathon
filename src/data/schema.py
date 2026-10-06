import pandas as pd

from src.data.profiler import profile_table
from src.data.relationship import find_possible_relationships

def extract_schema(df: pd.DataFrame) -> dict:
    """
    Extract logical data types for each DataFrame column.

    Returns:
        {
            "column_name": "logical_type"
        }
    """

    schema = {}

    for column in df.columns:

        if pd.api.types.is_bool_dtype(df[column]):
            data_type = "boolean"

        elif pd.api.types.is_numeric_dtype(df[column]):
            data_type = "number"

        else:
            converted = pd.to_datetime(
                df[column],
                errors="coerce",
                format="mixed"
            )

            valid_values = converted.notna().sum()

            if valid_values > 0 and valid_values / len(df) >= 0.8:
                data_type = "date"
            else:
                data_type = "string"

        schema[column] = data_type

    return schema


def build_table_profile(
    df: pd.DataFrame,
    table_name: str
) -> dict:
    """
    Build the complete profile for one table.

    Combines:
    - table name
    - row count
    - logical schema
    - data-quality information
    - dates
    - statistics
    - categories
    - currencies
    - units
    - warnings
    """

    # Get detailed profile information
    profile = profile_table(df)

    # Add logical schema information
    profile["name"] = table_name
    profile["columns"] = extract_schema(df)

    return profile

def build_multi_table_profile(
    tables: dict[str, pd.DataFrame]
) -> dict:
    """
    Build complete profiles for multiple tables.

    Also detects possible relationships between tables.
    """

    table_profiles = []

    for table_name, df in tables.items():

        table_profile = build_table_profile(
            df,
            table_name
        )

        table_profiles.append(table_profile)

    relationships = find_possible_relationships(tables)

    return {
        "tables": table_profiles,
        "relationships": relationships
    }

def build_data_profile(
    file_paths: list[str]
) -> dict:
    """
    Load multiple data files and build the complete
    Data -> Agent profile.

    Includes:
    - table profiles
    - schema information
    - missing values
    - duplicates
    - dates
    - statistics
    - categories
    - currencies
    - units
    - warnings
    - possible relationships
    """

    from src.data.loader import load_tables

    # Load all input tables
    tables = load_tables(file_paths)

    # Build complete multi-table profile
    profile = build_multi_table_profile(tables)

    return profile