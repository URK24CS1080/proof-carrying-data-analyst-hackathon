import pandas as pd

from src.data.currency import detect_currencies
from src.data.units import detect_units


def profile_table(df: pd.DataFrame) -> dict:
    """
    Create basic metadata for a single DataFrame.

    This function does not modify the original DataFrame.
    """

    # -----------------------------------------
    # 1. Detect date columns
    # -----------------------------------------
    date_columns = []

    for column in df.columns:

        # Do not treat numeric columns as dates
        if pd.api.types.is_numeric_dtype(df[column]):
            continue

        converted = pd.to_datetime(
            df[column],
            errors="coerce",
            format="mixed"
        )

        valid_values = converted.notna().sum()

        # Consider it a date column if at least 80%
        # of values can be converted to dates
        if len(df) > 0 and valid_values / len(df) >= 0.8:
            date_columns.append(column)

    # -----------------------------------------
    # 2. Detect date ranges
    # -----------------------------------------
    date_ranges = {}

    for column in date_columns:

        converted = pd.to_datetime(
            df[column],
            errors="coerce",
            format="mixed"
        )

        valid_dates = converted.dropna()

        if not valid_dates.empty:
            date_ranges[column] = {
                "min": valid_dates.min(),
                "max": valid_dates.max()
            }

    # -----------------------------------------
    # 3. Calculate numeric statistics
    # -----------------------------------------
    numeric_statistics = {}

    for column in df.columns:

        if pd.api.types.is_numeric_dtype(df[column]):

            numeric_statistics[column] = {
                "min": df[column].min(),
                "max": df[column].max(),
                "mean": df[column].mean()
            }

    # -----------------------------------------
    # 4. Detect categorical values
    # -----------------------------------------
    categorical_values = {}

    for column in df.columns:

        # Ignore numeric and date columns
        if (
            not pd.api.types.is_numeric_dtype(df[column])
            and column not in date_columns
        ):

            unique_values = df[column].dropna().unique()

            # Only store values for small categorical columns
            if len(unique_values) <= 20:

                categorical_values[column] = {
                    "unique_values": unique_values.tolist(),
                    "counts": df[column].value_counts().to_dict()
                }

    # -----------------------------------------
    # 5. Generate data-quality warnings
    # -----------------------------------------
    warnings = []

    # -----------------------------------------
    # 5A. Detect ambiguous date formats
    # -----------------------------------------
    for column in date_columns:

        for value in df[column].dropna():

            value = str(value).strip()

            # Detect formats such as:
            # 01/02/2026
            # 03-04-2026
            if (
                len(value) == 10
                and value[2] in ["/", "-"]
                and value[5] == value[2]
                and value[:2].isdigit()
                and value[3:5].isdigit()
                and value[6:].isdigit()
            ):

                first_part = int(value[:2])
                second_part = int(value[3:5])

                # Both parts can represent valid months
                if first_part <= 12 and second_part <= 12:

                    warnings.append(
                        f"Column '{column}' contains potentially "
                        "ambiguous date format(s)"
                    )

                    break

    # -----------------------------------------
    # 5B. Detect duplicate rows
    # -----------------------------------------
    duplicate_count = int(df.duplicated().sum())

    if duplicate_count > 0:

        warnings.append(
            f"Table contains {duplicate_count} duplicate row(s)"
        )

    # -----------------------------------------
    # 5C. Detect multiple units
    # -----------------------------------------
    detected_units = detect_units(df)

    for column, units in detected_units.items():

        if len(units) > 1:

            warnings.append(
                f"Column '{column}' contains multiple units: "
                f"{', '.join(units)}"
            )

    # -----------------------------------------
    # 5D. Detect multiple currencies
    # -----------------------------------------
    detected_currencies = detect_currencies(df)

    for column, currencies in detected_currencies.items():

        if len(currencies) > 1:

            warnings.append(
                f"Column '{column}' contains multiple currencies: "
                f"{', '.join(currencies)}"
            )

    # -----------------------------------------
    # 5E. Detect missing values
    # -----------------------------------------
    for column in df.columns:

        missing_count = int(df[column].isna().sum())

        if missing_count > 0:

            warnings.append(
                f"Column '{column}' contains "
                f"{missing_count} missing value(s)"
            )

    # -----------------------------------------
    # 6. Build final profile
    # -----------------------------------------
    profile = {

        "rows": len(df),

        "columns": len(df.columns),

        "column_names": list(df.columns),

        "data_types": {
            column: str(df[column].dtype)
            for column in df.columns
        },

        "missing_values": {
            column: int(df[column].isna().sum())
            for column in df.columns
        },

        "duplicate_rows": duplicate_count,

        "date_columns": date_columns,

        "date_ranges": date_ranges,

        "sample_rows": df.head(5).to_dict(
            orient="records"
        ),

        "numeric_statistics": numeric_statistics,

        "categorical_values": categorical_values,

        "currencies": detected_currencies,

        "units": detected_units,

        "warnings": warnings
    }

    return profile


def profile_tables(
    tables: dict[str, pd.DataFrame]
) -> dict:
    """
    Create profiles for multiple tables.

    Returns a dictionary where each key is the table name
    and each value is the profile of that table.
    """

    profiles = {}

    for table_name, df in tables.items():

        profiles[table_name] = profile_table(df)

    return profiles


def check_date_availability(
    df: pd.DataFrame,
    column: str,
    requested_date: str
) -> dict:
    """
    Check whether a requested date exists in a date column.

    Distinguishes between:
    - exact date exists
    - date is within overall range but has no row
    - date is outside the available range
    - invalid requested date
    """

    # Convert the column to datetime
    converted = pd.to_datetime(
        df[column],
        errors="coerce",
        format="mixed"
    )

    # Convert requested date
    requested = pd.to_datetime(
        requested_date,
        errors="coerce"
    )

    # -----------------------------------------
    # Invalid requested date
    # -----------------------------------------
    if pd.isna(requested):

        return {
            "available": False,
            "reason": "Invalid requested date"
        }

    # Keep only valid dates
    valid_dates = converted.dropna()

    # -----------------------------------------
    # No valid dates in column
    # -----------------------------------------
    if valid_dates.empty:

        return {
            "available": False,
            "reason": "No valid dates available in the column"
        }

    # -----------------------------------------
    # Find overall date range
    # -----------------------------------------
    minimum_date = valid_dates.min()
    maximum_date = valid_dates.max()

    # -----------------------------------------
    # Check exact date
    # -----------------------------------------
    exact_match = (
        valid_dates.dt.normalize()
        == requested.normalize()
    ).any()

    if exact_match:

        return {
            "available": True,
            "reason": "Requested date exists in the data",
            "available_from": minimum_date,
            "available_to": maximum_date
        }

    # -----------------------------------------
    # Date outside available range
    # -----------------------------------------
    if (
        requested < minimum_date
        or requested > maximum_date
    ):

        return {
            "available": False,
            "reason": "Requested date is outside the available data range",
            "available_from": minimum_date,
            "available_to": maximum_date
        }

    # -----------------------------------------
    # Date is inside range but does not exist
    # -----------------------------------------
    return {
        "available": False,
        "reason": (
            "Requested date is within the data range, "
            "but no data exists for this exact date"
        ),
        "available_from": minimum_date,
        "available_to": maximum_date
    }