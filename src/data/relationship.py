import pandas as pd


def find_possible_relationships(
    tables: dict[str, pd.DataFrame]
) -> list[dict]:
    """
    Find possible relationships between tables.

    A relationship is suggested when two columns:
    - have compatible data types
    - have enough overlapping non-null values

    This is only a possible relationship.
    It does not prove that a foreign-key relationship exists.
    """

    relationships = []

    table_names = list(tables.keys())

    for i in range(len(table_names)):

        table_a_name = table_names[i]
        table_a = tables[table_a_name]

        for j in range(i + 1, len(table_names)):

            table_b_name = table_names[j]
            table_b = tables[table_b_name]

            for column_a in table_a.columns:

                for column_b in table_b.columns:

                    # -----------------------------------------
                    # 1. Check compatible data types
                    # -----------------------------------------
                    numeric_a = pd.api.types.is_numeric_dtype(
                        table_a[column_a]
                    )

                    numeric_b = pd.api.types.is_numeric_dtype(
                        table_b[column_b]
                    )

                    if numeric_a != numeric_b:
                        continue

                    # -----------------------------------------
                    # 2. Get unique non-null values
                    # -----------------------------------------
                    values_a = set(
                        table_a[column_a].dropna().tolist()
                    )

                    values_b = set(
                        table_b[column_b].dropna().tolist()
                    )

                    if not values_a or not values_b:
                        continue

                    # -----------------------------------------
                    # 3. Find overlapping values
                    # -----------------------------------------
                    common_values = values_a & values_b

                    if not common_values:
                        continue

                    # -----------------------------------------
                    # 4. Calculate overlap ratio
                    # -----------------------------------------
                    smaller_set_size = min(
                        len(values_a),
                        len(values_b)
                    )

                    overlap_ratio = (
                        len(common_values) /
                        smaller_set_size
                    )

                    # -----------------------------------------
                    # 5. Require at least 50% overlap
                    # -----------------------------------------
                    if overlap_ratio >= 0.5:

                        relationships.append({
                            "table_a": table_a_name,
                            "column_a": column_a,
                            "table_b": table_b_name,
                            "column_b": column_b,
                            "common_values": len(common_values),
                            "overlap_ratio": round(
                                overlap_ratio,
                                2
                            ),
                            "reason": (
                                "compatible types and "
                                "sufficiently overlapping values"
                            )
                        })

    return relationships