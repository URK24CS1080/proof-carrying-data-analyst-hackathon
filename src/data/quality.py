import pandas as pd


NULL_MARKERS = {
    "null",
    "nan",
    "n/a",
    "na",
    "none",
}


def _detect_missing_values(df: pd.DataFrame) -> dict:
    """
    Detect missing values including:
    - Pandas-recognized missing values
    - Empty strings
    - Whitespace-only strings

    No data is modified.
    """

    columns = {}
    total_missing = 0

    for column in df.columns:
        missing_indexes = []

        for index, value in df[column].items():

            # Pandas-recognized missing value
            if pd.isna(value):
                missing_indexes.append(index)
                continue

            # Empty or whitespace-only string
            if isinstance(value, str) and not value.strip():
                missing_indexes.append(index)

        count = len(missing_indexes)

        if count > 0:
            columns[column] = {
                "count": count,
                "percentage": (
                    count / len(df) * 100
                    if len(df) > 0
                    else 0.0
                ),
                "row_indexes": missing_indexes,
                "status": "Needs analyst review",
                "detection_method": (
                    "Pandas isna() and blank-string detection"
                ),
                "recommendation": (
                    "Review the missing records before analysis."
                ),
                "action": (
                    "No automatic correction performed."
                ),
            }

            total_missing += count

    return {
        "total": total_missing,
        "columns": columns,
    }


def _detect_null_like_values(df: pd.DataFrame) -> dict:
    """
    Detect explicit null-like text representations.

    Examples:
    NULL, null, NaN, N/A, NA, None

    Only exact text matches after trimming and
    case normalization are considered.

    No data is modified.
    """

    total_null_like = 0
    columns = {}

    for column in df.columns:

        matching_indexes = []

        for index, value in df[column].items():

            if not isinstance(value, str):
                continue

            normalized = value.strip().lower()

            if normalized in NULL_MARKERS:
                matching_indexes.append(index)

        if matching_indexes:
            count = len(matching_indexes)

            columns[column] = {
                "count": count,
                "percentage": (
                    count / len(df) * 100
                    if len(df) > 0
                    else 0.0
                ),
                "values": sorted(
                    {
                        df.loc[index, column].strip()
                        for index in matching_indexes
                    }
                ),
                "row_indexes": list(matching_indexes),
                "status": "Needs analyst review",
                "detection_method": (
                    "Exact match against explicit "
                    "null-like text markers"
                ),
                "recommendation": (
                    "Review these values before analysis."
                ),
                "action": (
                    "No automatic correction performed."
                ),
            }

            total_null_like += count

    return {
        "total": total_null_like,
        "columns": columns,
    }


def _detect_duplicates(df: pd.DataFrame) -> dict:
    """
    Detect duplicate rows without removing them.

    No data is modified.
    """

    duplicate_mask = df.duplicated(keep="first")

    duplicate_indexes = df.index[
        duplicate_mask
    ].tolist()

    duplicate_count = len(duplicate_indexes)

    return {
        "count": duplicate_count,
        "percentage": (
            duplicate_count / len(df) * 100
            if len(df) > 0
            else 0.0
        ),
        "row_indexes": duplicate_indexes,
        "status": (
            "Needs analyst review"
            if duplicate_count > 0
            else "No duplicates detected"
        ),
        "detection_method": (
            "Pandas duplicated()"
        ),
        "recommendation": (
            "Review duplicate records before analysis."
        ),
        "action": (
            "No duplicate rows were removed."
        ),
    }


def _detect_outliers(df: pd.DataFrame) -> dict:
    """
    Detect potential outliers in numerical columns
    using the IQR method.

    IQR = Q3 - Q1
    Lower bound = Q1 - 1.5 * IQR
    Upper bound = Q3 + 1.5 * IQR

    No data is modified.
    """

    outliers = {}

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:

        series = df[column].dropna()

        if series.empty:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outlier_mask = (
            (df[column] < lower_bound)
            | (df[column] > upper_bound)
        )

        outlier_mask = outlier_mask.fillna(False)

        row_indexes = df.index[
            outlier_mask
        ].tolist()

        outlier_count = len(row_indexes)

        if outlier_count > 0:
            outliers[column] = {
                "count": outlier_count,
                "percentage": (
                    outlier_count / len(df) * 100
                    if len(df) > 0
                    else 0.0
                ),
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound),
                "row_indexes": row_indexes,
                "method": "IQR",
                "status": "Needs analyst review",
                "reason": (
                    "Values fall outside the calculated "
                    "IQR bounds."
                ),
                "recommendation": (
                    "Review these observations before "
                    "using this column for analysis."
                ),
                "action": (
                    "No outlier values were removed "
                    "or changed."
                ),
            }

    return outliers


def _classify_value(value) -> str:
    """
    Classify a value into a simple semantic type.

    No data is modified.
    """

    if isinstance(value, bool):
        return "boolean"

    if (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
    ):
        return "number"

    if isinstance(value, pd.Timestamp):
        return "date"

    if isinstance(value, str):

        text = value.strip()

        if not text:
            return "empty"

        numeric_value = pd.to_numeric(
            text,
            errors="coerce"
        )

        if pd.notna(numeric_value):
            return "number"

        date_value = pd.to_datetime(
            text,
            errors="coerce",
            format="mixed"
        )

        if pd.notna(date_value):
            return "date"

        return "string"

    return type(value).__name__


def _detect_type_issues(df: pd.DataFrame) -> list:
    """
    Detect obvious mixed semantic types within columns.

    No automatic conversion is performed.
    """

    issues = []

    for column in df.columns:

        classifications = {}
        row_indexes = {}

        for index, value in df[column].items():

            if pd.isna(value):
                continue

            if isinstance(value, str):
                normalized = value.strip().lower()

                if normalized in NULL_MARKERS:
                    continue

            value_type = _classify_value(value)

            if value_type == "empty":
                continue

            classifications.setdefault(
                value_type,
                []
            ).append(value)

            row_indexes.setdefault(
                value_type,
                []
            ).append(index)

        detected_types = set(
            classifications.keys()
        )

        if len(detected_types) <= 1:
            continue

        affected_indexes = []

        for indexes in row_indexes.values():
            affected_indexes.extend(indexes)

        issues.append({
            "column": column,
            "detected_types": sorted(
                detected_types
            ),
            "row_indexes": affected_indexes,
            "status": "Needs analyst review",
            "detection_method": (
                "Semantic type classification "
                "without automatic conversion"
            ),
            "reason": (
                "The column contains values belonging "
                "to different semantic types."
            ),
            "recommendation": (
                "Review the inconsistent values and "
                "decide how they should be handled."
            ),
            "action": (
                "No values were converted, replaced, "
                "or removed."
            ),
        })

    return issues


def _detect_categorical_inconsistencies(
    df: pd.DataFrame
) -> list:
    """
    Detect categorical formatting variations.

    Variations are identified using:
    - trimming whitespace
    - case-insensitive comparison

    No data is modified.
    """

    issues = {}

    for column in df.columns:

        values = df[column]

        if not (
            pd.api.types.is_object_dtype(values)
            or pd.api.types.is_string_dtype(values)
        ):
            continue

        groups = {}

        for index, value in values.items():

            if not isinstance(value, str):
                continue

            stripped = value.strip()

            if not stripped:
                continue

            if stripped.lower() in NULL_MARKERS:
                continue

            normalized = stripped.casefold()

            groups.setdefault(
                normalized,
                []
            ).append({
                "value": value,
                "row_index": index,
            })

        for normalized, variants in groups.items():

            unique_values = sorted(
                {
                    item["value"]
                    for item in variants
                }
            )

            if len(unique_values) <= 1:
                continue

            issues.setdefault(
                column,
                []
            ).append({
                "normalized_value": normalized,
                "variants": unique_values,
                "row_indexes": [
                    item["row_index"]
                    for item in variants
                ],
                "status": "Needs analyst review",
                "detection_method": (
                    "Case-insensitive and "
                    "whitespace-normalized comparison"
                ),
                "reason": (
                    "Multiple textual representations "
                    "appear to refer to the same "
                    "normalized category."
                ),
                "recommendation": (
                    "Review these category variants "
                    "and decide whether they should "
                    "be standardized."
                ),
                "action": (
                    "No categorical values were "
                    "normalized or changed."
                ),
            })

    return [
        {
            "column": column,
            "variations": variations,
        }
        for column, variations in issues.items()
    ]


def _detect_empty_rows_and_columns(
    df: pd.DataFrame
) -> dict:
    """
    Detect completely empty rows and columns.

    Empty means:
    - Pandas missing value
    - blank string
    - whitespace-only string

    No data is modified.
    """

    empty_mask = df.copy()

    for column in empty_mask.columns:

        empty_mask[column] = empty_mask[column].apply(
            lambda value: (
                True
                if pd.isna(value)
                else (
                    True
                    if isinstance(value, str)
                    and not value.strip()
                    else False
                )
            )
        )

    empty_rows_mask = empty_mask.all(axis=1)

    empty_row_indexes = df.index[
        empty_rows_mask
    ].tolist()

    empty_columns_mask = empty_mask.all(axis=0)

    empty_columns = df.columns[
        empty_columns_mask
    ].tolist()

    return {
        "empty_rows": {
            "count": len(empty_row_indexes),
            "row_indexes": empty_row_indexes,
            "status": (
                "Needs analyst review"
                if empty_row_indexes
                else "No completely empty rows detected"
            ),
            "detection_method": (
                "Rows where all values are missing "
                "or blank"
            ),
            "recommendation": (
                "Review completely empty rows "
                "before analysis."
            ),
            "action": (
                "No rows were removed."
            ),
        },
        "empty_columns": {
            "count": len(empty_columns),
            "columns": empty_columns,
            "status": (
                "Needs analyst review"
                if empty_columns
                else "No completely empty columns detected"
            ),
            "detection_method": (
                "Columns where all values are missing "
                "or blank"
            ),
            "recommendation": (
                "Review completely empty columns "
                "before analysis."
            ),
            "action": (
                "No columns were removed."
            ),
        },
    }


def _detect_constant_columns(
    df: pd.DataFrame
) -> list:
    """
    Detect columns containing only one unique
    non-missing value.

    No data is modified.
    """

    constant_columns = []

    for column in df.columns:

        non_missing = df[column].dropna()

        if non_missing.empty:
            continue

        unique_count = non_missing.nunique(
            dropna=True
        )

        if unique_count == 1:

            constant_columns.append({
                "column": column,
                "unique_values": [
                    non_missing.iloc[0]
                ],
                "status": "Needs analyst review",
                "detection_method": (
                    "One unique non-missing value"
                ),
                "reason": (
                    "The column contains only one "
                    "distinct non-missing value."
                ),
                "recommendation": (
                    "Review whether this column provides "
                    "useful variation for analysis."
                ),
                "action": (
                    "No column or values were removed."
                ),
            })

    return constant_columns


def _calculate_summary(report: dict) -> dict:
    """
    Calculate a simple overall issue summary.

    No data is modified.
    """

    issue_count = 0

    issue_count += report["missing_values"].get(
        "total", 0
    )

    issue_count += report["null_values"].get(
        "total", 0
    )

    issue_count += report["duplicates"].get(
        "count", 0
    )

    for details in report["outliers"].values():
        issue_count += details.get("count", 0)

    issue_count += len(
        report["type_issues"]
    )

    for item in report["inconsistencies"]:
        issue_count += len(
            item.get("variations", [])
        )

    issue_count += report["empty_rows"].get(
        "count", 0
    )

    issue_count += report["empty_columns"].get(
        "count", 0
    )

    issue_count += len(
        report["constant_columns"]
    )

    return {
        "has_issues": issue_count > 0,
        "total_issues": issue_count,
    }


def analyze_data_quality(
    df: pd.DataFrame
) -> dict:
    """
    Analyze a DataFrame for potential
    data-quality issues.

    This function only detects and reports issues.
    It does not modify the input DataFrame.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "analyze_data_quality() expects "
            "a pandas DataFrame."
        )

    report = {
        "summary": {
            "has_issues": False,
            "total_issues": 0,
        },
        "missing_values": {},
        "null_values": {},
        "duplicates": {},
        "outliers": {},
        "type_issues": [],
        "inconsistencies": [],
        "empty_rows": {},
        "empty_columns": {},
        "constant_columns": [],
    }

    report["missing_values"] = (
        _detect_missing_values(df)
    )

    report["null_values"] = (
        _detect_null_like_values(df)
    )

    report["duplicates"] = (
        _detect_duplicates(df)
    )

    report["outliers"] = (
        _detect_outliers(df)
    )

    report["type_issues"] = (
        _detect_type_issues(df)
    )

    report["inconsistencies"] = (
        _detect_categorical_inconsistencies(df)
    )

    empty_structure = (
        _detect_empty_rows_and_columns(df)
    )

    report["empty_rows"] = (
        empty_structure["empty_rows"]
    )

    report["empty_columns"] = (
        empty_structure["empty_columns"]
    )

    report["constant_columns"] = (
        _detect_constant_columns(df)
    )

    report["summary"] = (
        _calculate_summary(report)
    )

    return report