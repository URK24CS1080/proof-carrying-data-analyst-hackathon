def generate_proof(plan: dict) -> str:
    """
    Generate deterministic, runnable Python proof code
    from a validated execution plan.

    The proof code is generated only from approved
    operations and structured plan fields.

    The LLM does not generate this code.
    """

    if not isinstance(plan, dict):
        raise ValueError(
            "Plan must be a dictionary."
        )

    if plan.get("status") != "answerable":
        raise ValueError(
            "Proof can only be generated for an answerable plan."
        )

    operation = plan.get("operation")
    table = plan.get("table")
    column = plan.get("column")
    filters = plan.get("filters") or {}
    date_filter = plan.get("date_filter")
    group_by = plan.get("group_by")
    sort_order = plan.get("sort")
    limit = plan.get("limit")
    join_config = plan.get("join")

    if not operation:
        raise ValueError(
            "Plan is missing an operation."
        )

    if not table:
        raise ValueError(
            "Plan is missing a table."
        )

    if not column:
        raise ValueError(
            "Plan is missing a column."
        )

    supported_operations = {
        "average",
        "count",
        "sum",
        "min",
        "max",
        "group_average",
    }

    if operation not in supported_operations:
        raise ValueError(
            f"Proof generation for operation '{operation}' "
            "is not supported yet."
        )

    lines = []

    # --------------------------------------------------
    # LOAD MAIN TABLE
    # --------------------------------------------------

    lines.append(
        f'df = tables["{table}"].copy()'
    )

    # --------------------------------------------------
    # APPLY INNER JOIN
    # --------------------------------------------------

    if join_config is not None:

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
                "Join configuration requires 'table'."
            )

        if not left_on:
            raise ValueError(
                "Join configuration requires 'left_on'."
            )

        if not right_on:
            raise ValueError(
                "Join configuration requires 'right_on'."
            )

        if how != "inner":
            raise ValueError(
                "Only 'inner' JOIN is supported."
            )

        lines.append(
            f'df = df.merge('
            f'tables[{join_table!r}].copy(), '
            f'left_on={left_on!r}, '
            f'right_on={right_on!r}, '
            f'how="inner"'
            f')'
        )

    # --------------------------------------------------
    # APPLY NORMAL FILTERS
    # --------------------------------------------------

    for filter_column, filter_value in filters.items():

        if isinstance(filter_value, str):
            value_repr = repr(filter_value)

        elif isinstance(
            filter_value,
            (int, float, bool)
        ):
            value_repr = repr(filter_value)

        elif filter_value is None:
            value_repr = "None"

        else:
            raise ValueError(
                f"Unsupported filter value for "
                f"'{filter_column}'."
            )

        lines.append(
            f"df = df[df[{filter_column!r}] == {value_repr}]"
        )

    # --------------------------------------------------
    # APPLY DATE FILTER
    # --------------------------------------------------

    if date_filter is not None:

        if not isinstance(date_filter, dict):
            raise ValueError(
                "Date filter must be a dictionary."
            )

        date_column = date_filter.get("column")
        start = date_filter.get("start")
        end = date_filter.get("end")

        if not date_column:
            raise ValueError(
                "Date filter requires 'column'."
            )

        if start is None and end is None:
            raise ValueError(
                "Date filter requires 'start' or 'end'."
            )

        lines.append(
            f"df[{date_column!r}] = "
            f"__import__('pandas').to_datetime("
            f"df[{date_column!r}], "
            f"errors='coerce'"
            f")"
        )

        if start is not None:

            lines.append(
                f"df = df["
                f"df[{date_column!r}] >= "
                f"__import__('pandas').to_datetime("
                f"{start!r}"
                f")"
                f"]"
            )

        if end is not None:

            lines.append(
                f"df = df["
                f"df[{date_column!r}] <= "
                f"__import__('pandas').to_datetime("
                f"{end!r}"
                f")"
                f"]"
            )

    # --------------------------------------------------
    # GROUP AVERAGE
    # --------------------------------------------------

    if operation == "group_average":

        if not group_by:
            raise ValueError(
                "GROUP AVERAGE proof requires "
                "'group_by'."
            )

        lines.append(
            f"df = ("
            f"df.dropna(subset=[{column!r}])"
            f".groupby({group_by!r}, dropna=False)"
            f"[{column!r}]"
            f".mean()"
            f".reset_index(name='average')"
            f")"
        )

        # --------------------------------------------------
        # SORT GROUP RESULT
        # --------------------------------------------------

        if sort_order is not None:

            if sort_order not in {
                "ascending",
                "descending"
            }:
                raise ValueError(
                    "Sort must be either "
                    "'ascending' or 'descending'."
                )

            descending = (
                sort_order == "descending"
            )

            lines.append(
                "df = df.sort_values("
                "by='average', "
                f"ascending={not descending}"
                ").reset_index(drop=True)"
            )

        # --------------------------------------------------
        # TOP N
        # --------------------------------------------------

        if limit is not None:

            if not isinstance(limit, int):
                raise ValueError(
                    "Limit must be an integer."
                )

            if limit <= 0:
                raise ValueError(
                    "Limit must be greater than zero."
                )

            lines.append(
                f"df = df.head({limit}).copy()"
            )

        lines.append(
            "answer = df"
        )

    # --------------------------------------------------
    # SIMPLE OPERATIONS
    # --------------------------------------------------

    elif operation == "average":

        lines.append(
            f"answer = df[{column!r}].dropna().mean()"
        )

    elif operation == "count":

        lines.append(
            f"answer = df[{column!r}].count()"
        )

    elif operation == "sum":

        lines.append(
            f"answer = df[{column!r}].dropna().sum()"
        )

    elif operation == "min":

        lines.append(
            f"answer = df[{column!r}].dropna().min()"
        )

    elif operation == "max":

        lines.append(
            f"answer = df[{column!r}].dropna().max()"
        )

    lines.append(
        "print(answer)"
    )

    return "\n".join(lines)