import pandas as pd

from .operations import (
    average,
    count,
    sum_values,
    minimum,
    maximum,
    group_average,
    apply_filters,
    apply_date_filter,
    sort_values,
    top_n,
    join_tables,
)


SUPPORTED_OPERATIONS = {
    "average": average,
    "count": count,
    "sum": sum_values,
    "min": minimum,
    "max": maximum,
    "group_average": group_average,
}


def execute_plan(
    plan: dict,
    tables: dict[str, pd.DataFrame]
) -> dict:
    """
    Execute a structured analysis plan using controlled operations.

    The executor never runs arbitrary Python code.
    It only uses approved operations.
    """

    # 1. Validate plan type
    if not isinstance(plan, dict):
        return {
            "status": "execution_error",
            "answer": None,
            "reason": "Execution plan must be a dictionary.",
        }

    # 2. Handle plans that are not answerable
    if plan.get("status") != "answerable":
        return {
            "status": plan.get("status", "execution_error"),
            "answer": None,
            "reason": plan.get(
                "reason",
                "Plan is not answerable."
            ),
        }

    # 3. Read plan fields
    operation = plan.get("operation")
    table_name = plan.get("table")
    column = plan.get("column")
    filters = plan.get("filters")
    date_filter = plan.get("date_filter")
    group_by = plan.get("group_by")
    sort_order = plan.get("sort")
    limit = plan.get("limit")
    join_config = plan.get("join")

    # 4. Validate operation
    if operation not in SUPPORTED_OPERATIONS:
        return {
            "status": "execution_error",
            "answer": None,
            "reason": f"Unsupported operation: {operation}",
        }

    # 5. Validate table
    if table_name not in tables:
        return {
            "status": "execution_error",
            "answer": None,
            "reason": f"Table '{table_name}' does not exist.",
        }

    # 6. Validate column
    if not column:
        return {
            "status": "execution_error",
            "answer": None,
            "reason": "No column was provided.",
        }

    # 7. Work on a copy of the original data
    df = tables[table_name].copy()

    try:

        # 8. Apply JOIN
        if join_config:

            if not isinstance(join_config, dict):
                raise ValueError(
                    "Join configuration must be a dictionary."
                )

            join_table = join_config.get("table")
            left_on = join_config.get("left_on")
            right_on = join_config.get("right_on")
            how = join_config.get("how", "inner")

            if not join_table:
                raise ValueError(
                    "Join configuration requires a table."
                )

            if join_table not in tables:
                raise ValueError(
                    f"Join table '{join_table}' does not exist."
                )

            if not left_on:
                raise ValueError(
                    "Join configuration requires 'left_on'."
                )

            if not right_on:
                raise ValueError(
                    "Join configuration requires 'right_on'."
                )

            df = join_tables(
                left_df=df,
                right_df=tables[join_table].copy(),
                left_on=left_on,
                right_on=right_on,
                how=how,
            )

        # 9. Apply equality filters
        df = apply_filters(
            df,
            filters
        )

        # 10. Apply date filter
        if date_filter:

            if not isinstance(date_filter, dict):
                raise ValueError(
                    "Date filter must be provided as a dictionary."
                )

            date_column = date_filter.get("column")
            start = date_filter.get("start")
            end = date_filter.get("end")

            if not date_column:
                raise ValueError(
                    "Date filter requires a column."
                )

            df = apply_date_filter(
                df=df,
                column=date_column,
                start=start,
                end=end,
            )

        # 11. Handle zero matching rows
        if df.empty:
            return {
                "status": "cannot_determine",
                "answer": None,
                "reason": "The applied filters matched no rows.",
                "operation": operation,
                "table": table_name,
                "column": column,
                "group_by": group_by,
                "filters": filters or {},
                "date_filter": date_filter,
                "sort": sort_order,
                "limit": limit,
                "join": join_config,
                "rows_analyzed": 0,
            }

        # 12. Execute main operation
        if operation == "group_average":

            if not group_by:
                raise ValueError(
                    "GROUP BY operation requires a 'group_by' column."
                )

            answer = group_average(
                df=df,
                column=column,
                group_by=group_by,
            )

        else:

            operation_function = SUPPORTED_OPERATIONS[operation]

            answer = operation_function(
                df=df,
                column=column,
            )

        # 13. Apply SORT and TOP N
        if sort_order is not None or limit is not None:

            if not isinstance(answer, pd.DataFrame):
                raise ValueError(
                    "SORT and TOP N can only be applied to tabular results."
                )

            if sort_order is not None:

                if sort_order not in {
                    "ascending",
                    "descending"
                }:
                    raise ValueError(
                        "Sort must be either 'ascending' or 'descending'."
                    )

                if "average" in answer.columns:
                    sort_column = "average"
                else:
                    raise ValueError(
                        "No supported result column is available for sorting."
                    )

                answer = sort_values(
                    df=answer,
                    column=sort_column,
                    descending=(sort_order == "descending"),
                )

            if limit is not None:

                if not isinstance(limit, int):
                    raise ValueError(
                        "Limit must be an integer."
                    )

                answer = top_n(
                    df=answer,
                    n=limit,
                )

        # 14. Successful execution result
        return {
            "status": "executed",
            "answer": answer,
            "operation": operation,
            "table": table_name,
            "column": column,
            "group_by": group_by,
            "filters": filters or {},
            "date_filter": date_filter,
            "sort": sort_order,
            "limit": limit,
            "join": join_config,
            "rows_analyzed": len(df),
        }

    except Exception as exc:

        # 15. Controlled execution error
        return {
            "status": "execution_error",
            "answer": None,
            "reason": str(exc),
            "operation": operation,
            "table": table_name,
            "column": column,
            "group_by": group_by,
            "filters": filters or {},
            "date_filter": date_filter,
            "sort": sort_order,
            "limit": limit,
            "join": join_config,
        }