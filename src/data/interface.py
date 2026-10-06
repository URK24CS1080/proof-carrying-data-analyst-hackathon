from typing import Any


def create_agent_data_contract(
    data_profile: dict
) -> dict[str, Any]:
    """
    Convert the internal data profile into the
    Data -> Agent contract.

    The contract describes:
    - available tables
    - rows
    - columns and logical types
    - missing values
    - duplicates
    - dates
    - statistics
    - categories
    - currencies
    - units
    - samples
    - warnings
    - possible relationships

    This function does not modify the original profile.
    """

    tables = []

    for table in data_profile.get("tables", []):

        table_contract = {
            "name": table.get("name"),
            "rows": table.get("rows"),
            "columns": table.get("columns", {}),
            "missing_values": table.get(
                "missing_values",
                {}
            ),
            "duplicate_rows": table.get(
                "duplicate_rows",
                0
            ),
            "date_columns": table.get(
                "date_columns",
                []
            ),
            "date_ranges": table.get(
                "date_ranges",
                {}
            ),
            "numeric_statistics": table.get(
                "numeric_statistics",
                {}
            ),
            "categorical_values": table.get(
                "categorical_values",
                {}
            ),
            "currencies": table.get(
                "currencies",
                {}
            ),
            "units": table.get(
                "units",
                {}
            ),
            "sample_rows": table.get(
                "sample_rows",
                []
            ),
            "warnings": table.get(
                "warnings",
                []
            )
        }

        tables.append(table_contract)

    return {
    "tables": tables,
    "relationships": data_profile.get(
        "relationships",
        []
    ),
    "contradictions": data_profile.get(
        "contradictions",
        []
    )
}