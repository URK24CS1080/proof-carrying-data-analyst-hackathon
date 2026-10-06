import pandas as pd


def apply_filters(
    df: pd.DataFrame,
    filters: dict | None = None
) -> pd.DataFrame:
    """
    Apply simple equality filters to a DataFrame.

    Example:
        filters = {
            "category": "Electronics"
        }

    Returns:
        A filtered copy of the DataFrame.
    """

    if not filters:
        return df.copy()

    if not isinstance(filters, dict):
        raise ValueError("Filters must be provided as a dictionary.")

    filtered_df = df.copy()

    for column, value in filters.items():

        if column not in filtered_df.columns:
            raise ValueError(
                f"Filter column '{column}' does not exist."
            )

        filtered_df = filtered_df[
            filtered_df[column] == value
        ]

    return filtered_df


def average(
    df: pd.DataFrame,
    column: str
) -> float:
    """
    Calculate the average of a numeric column.

    Missing values are ignored.

    Raises:
        ValueError:
            If the column does not exist or contains no valid values.

        TypeError:
            If the remaining values are not numeric.
    """

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    # Remove missing values first.
    values = df[column].dropna()

    # If nothing remains, there is no usable data.
    if values.empty:
        raise ValueError(
            f"Column '{column}' contains no valid values for calculation."
        )

    # Check the remaining values.
    if not pd.api.types.is_numeric_dtype(values):
        raise TypeError(
            f"Column '{column}' must contain numeric values."
        )

    return float(values.mean())

def count(
    df: pd.DataFrame,
    column: str
) -> int:
    """
    Count non-missing values in a column.

    Missing values are not counted.
    """

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    return int(df[column].count())

def sum_values(
    df: pd.DataFrame,
    column: str
) -> float:
    """
    Calculate the sum of a numeric column.

    Missing values are ignored.
    """

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    values = df[column].dropna()

    if values.empty:
        raise ValueError(
            f"Column '{column}' contains no valid values for calculation."
        )

    if not pd.api.types.is_numeric_dtype(values):
        raise TypeError(
            f"Column '{column}' must contain numeric values."
        )

    return float(values.sum())

def minimum(
    df: pd.DataFrame,
    column: str
) -> float:
    """
    Find the minimum value in a numeric column.

    Missing values are ignored.
    """

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    values = df[column].dropna()

    if values.empty:
        raise ValueError(
            f"Column '{column}' contains no valid values for calculation."
        )

    if not pd.api.types.is_numeric_dtype(values):
        raise TypeError(
            f"Column '{column}' must contain numeric values."
        )

    return float(values.min())


def maximum(
    df: pd.DataFrame,
    column: str
) -> float:
    """
    Find the maximum value in a numeric column.

    Missing values are ignored.
    """

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    values = df[column].dropna()

    if values.empty:
        raise ValueError(
            f"Column '{column}' contains no valid values for calculation."
        )

    if not pd.api.types.is_numeric_dtype(values):
        raise TypeError(
            f"Column '{column}' must contain numeric values."
        )

    return float(values.max())

def apply_date_filter(
    df: pd.DataFrame,
    column: str,
    start: str | None = None,
    end: str | None = None
) -> pd.DataFrame:
    """
    Apply a controlled date-range filter.

    Args:
        df: Input DataFrame.
        column: Date column.
        start: Inclusive start date.
        end: Inclusive end date.

    Returns:
        Filtered copy of the DataFrame.
    """

    if column not in df.columns:
        raise ValueError(
            f"Date column '{column}' does not exist."
        )

    if start is None and end is None:
        raise ValueError(
            "At least one of 'start' or 'end' must be provided."
        )

    filtered_df = df.copy()

    # Convert the date column once.
    dates = pd.to_datetime(
        filtered_df[column],
        errors="coerce"
    )

    if dates.notna().sum() == 0:
        raise ValueError(
            f"Date column '{column}' contains no valid dates."
        )

    mask = pd.Series(
        True,
        index=filtered_df.index
    )

    if start is not None:
        try:
            start_date = pd.to_datetime(start)
        except Exception:
            raise ValueError(
                f"Invalid start date: '{start}'."
            )

        mask &= dates >= start_date

    if end is not None:
        try:
            end_date = pd.to_datetime(end)
        except Exception:
            raise ValueError(
                f"Invalid end date: '{end}'."
            )

        mask &= dates <= end_date

    return filtered_df.loc[mask].copy()

def group_average(
    df: pd.DataFrame,
    column: str,
    group_by: str
) -> pd.DataFrame:
    """
    Calculate the average of a numeric column for each group.

    Example:
        group_average(
            df,
            column="revenue",
            group_by="category"
        )

    Returns:
        DataFrame containing the group and calculated average.
    """

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    if group_by not in df.columns:
        raise ValueError(
            f"Group-by column '{group_by}' does not exist."
        )

    values = df[column].dropna()

    if values.empty:
        raise ValueError(
            f"Column '{column}' contains no valid values for calculation."
        )

    if not pd.api.types.is_numeric_dtype(values):
        raise TypeError(
            f"Column '{column}' must contain numeric values."
        )

    result = (
        df.dropna(subset=[column])
        .groupby(group_by, dropna=False)[column]
        .mean()
        .reset_index(name="average")
    )

    if result.empty:
        raise ValueError(
            "No valid groups were available for calculation."
        )

    return result

def sort_values(
    df: pd.DataFrame,
    column: str,
    descending: bool = False
) -> pd.DataFrame:
    """
    Sort a DataFrame by a specified column.

    Args:
        df: Input DataFrame.
        column: Column to sort by.
        descending: If True, sort from highest to lowest.

    Returns:
        A sorted copy of the DataFrame.
    """

    if column not in df.columns:
        raise ValueError(
            f"Sort column '{column}' does not exist."
        )

    if df.empty:
        raise ValueError(
            "Cannot sort an empty DataFrame."
        )

    return df.sort_values(
        by=column,
        ascending=not descending
    ).reset_index(drop=True)

def top_n(
    df: pd.DataFrame,
    n: int
) -> pd.DataFrame:
    """
    Return the first N rows of a DataFrame.

    The DataFrame is expected to already be sorted
    if the caller wants the highest or lowest values.

    Args:
        df: Input DataFrame.
        n: Number of rows to return.

    Returns:
        A copy containing at most N rows.
    """

    if not isinstance(n, int):
        raise ValueError(
            "TOP N value must be an integer."
        )

    if n <= 0:
        raise ValueError(
            "TOP N value must be greater than zero."
        )

    if df.empty:
        raise ValueError(
            "Cannot select TOP N from an empty DataFrame."
        )

    return df.head(n).copy()

def join_tables(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    left_on: str,
    right_on: str,
    how: str = "inner"
) -> pd.DataFrame:
    """
    Perform a controlled table join.

    Only supported join type for the MVP is INNER JOIN.

    Args:
        left_df: Left DataFrame.
        right_df: Right DataFrame.
        left_on: Join column from the left DataFrame.
        right_on: Join column from the right DataFrame.
        how: Join type.

    Returns:
        Joined DataFrame.
    """

    if not isinstance(left_df, pd.DataFrame):
        raise ValueError(
            "Left table must be a pandas DataFrame."
        )

    if not isinstance(right_df, pd.DataFrame):
        raise ValueError(
            "Right table must be a pandas DataFrame."
        )

    if left_on not in left_df.columns:
        raise ValueError(
            f"Left join column '{left_on}' does not exist."
        )

    if right_on not in right_df.columns:
        raise ValueError(
            f"Right join column '{right_on}' does not exist."
        )

    if how != "inner":
        raise ValueError(
            "Only 'inner' JOIN is supported."
        )

    if left_df.empty:
        raise ValueError(
            "Cannot join an empty left table."
        )

    if right_df.empty:
        raise ValueError(
            "Cannot join an empty right table."
        )

    return left_df.merge(
        right_df,
        left_on=left_on,
        right_on=right_on,
        how="inner"
    )