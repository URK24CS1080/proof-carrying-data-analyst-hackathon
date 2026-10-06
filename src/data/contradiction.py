import pandas as pd


def find_contradictions(
    table_a: pd.DataFrame,
    table_b: pd.DataFrame,
    key_column_a: str,
    key_column_b: str,
    value_column_a: str,
    value_column_b: str
) -> list[dict]:
    """
    Find conflicting values between two related tables.

    The key columns identify the same record.
    The value columns are compared for contradictions.

    Example:

        Table A:
        customer_id | city
        1            | Chennai

        Table B:
        customer_id | city
        1            | Bangalore

    Result:
        customer_id 1 has conflicting city values.

    The original DataFrames are not modified.
    """

    required_a = {key_column_a, value_column_a}
    required_b = {key_column_b, value_column_b}

    if not required_a.issubset(table_a.columns):
        raise ValueError(
            f"Missing required columns in table A: "
            f"{required_a - set(table_a.columns)}"
        )

    if not required_b.issubset(table_b.columns):
        raise ValueError(
            f"Missing required columns in table B: "
            f"{required_b - set(table_b.columns)}"
        )

    left = table_a[
        [key_column_a, value_column_a]
    ].dropna(
        subset=[key_column_a, value_column_a]
    )

    right = table_b[
        [key_column_b, value_column_b]
    ].dropna(
        subset=[key_column_b, value_column_b]
    )

    merged = left.merge(
        right,
        left_on=key_column_a,
        right_on=key_column_b,
        how="inner",
        suffixes=("_a", "_b")
    )

    contradictions = []

    for _, row in merged.iterrows():

        value_a = row[f"{value_column_a}_a"]
        value_b = row[f"{value_column_b}_b"]

        if value_a != value_b:

            contradictions.append({
                "key": row[key_column_a],
                "value_a": value_a,
                "value_b": value_b,
                "reason": "Conflicting values for the same key"
            })

    return contradictions