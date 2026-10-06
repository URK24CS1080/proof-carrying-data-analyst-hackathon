import math

import pandas as pd


def compare_results(
    expected,
    actual,
    tolerance: float = 1e-9,
) -> dict:
    """
    Compare an executor result with an independently
    executed proof result.

    Supports:
    - numbers
    - strings
    - booleans
    - pandas DataFrames
    - None
    """

    # --------------------------------------------------
    # CASE 1 — BOTH ARE NONE
    # --------------------------------------------------

    if expected is None and actual is None:
        return {
            "matched": True,
            "reason": "Both results are None.",
        }

    # --------------------------------------------------
    # CASE 2 — ONE IS NONE
    # --------------------------------------------------

    if expected is None or actual is None:
        return {
            "matched": False,
            "reason": "One result is None while the other is not.",
        }

    # --------------------------------------------------
    # CASE 3 — DATAFRAME RESULTS
    # --------------------------------------------------

    if isinstance(expected, pd.DataFrame) or isinstance(
        actual,
        pd.DataFrame,
    ):

        if not isinstance(expected, pd.DataFrame):
            return {
                "matched": False,
                "reason": "Only the proof result is a DataFrame.",
            }

        if not isinstance(actual, pd.DataFrame):
            return {
                "matched": False,
                "reason": "Only the executor result is a DataFrame.",
            }

        expected_df = expected.reset_index(drop=True)
        actual_df = actual.reset_index(drop=True)

        if list(expected_df.columns) != list(actual_df.columns):
            return {
                "matched": False,
                "reason": "DataFrame columns do not match.",
            }

        if expected_df.shape != actual_df.shape:
            return {
                "matched": False,
                "reason": "DataFrame shapes do not match.",
            }

        try:
            pd.testing.assert_frame_equal(
                expected_df,
                actual_df,
                check_dtype=False,
                check_exact=False,
                rtol=tolerance,
                atol=tolerance,
            )

            return {
                "matched": True,
                "reason": "DataFrame results match.",
            }

        except AssertionError as exc:
            return {
                "matched": False,
                "reason": f"DataFrame values do not match: {exc}",
            }

    # --------------------------------------------------
    # CASE 4 — NUMERIC RESULTS
    # --------------------------------------------------

    if isinstance(expected, (int, float)) and isinstance(
        actual,
        (int, float),
    ):

        if isinstance(expected, bool) or isinstance(actual, bool):
            return {
                "matched": expected == actual,
                "reason": (
                    "Boolean results match."
                    if expected == actual
                    else "Boolean results do not match."
                ),
            }

        if math.isclose(
            float(expected),
            float(actual),
            rel_tol=tolerance,
            abs_tol=tolerance,
        ):
            return {
                "matched": True,
                "reason": "Numeric results match within tolerance.",
            }

        return {
            "matched": False,
            "reason": (
                f"Numeric results differ: "
                f"expected={expected}, actual={actual}."
            ),
        }

    # --------------------------------------------------
    # CASE 5 — OTHER SIMPLE VALUES
    # --------------------------------------------------

    if expected == actual:
        return {
            "matched": True,
            "reason": "Results match.",
        }

    return {
        "matched": False,
        "reason": (
            f"Results differ: "
            f"expected={expected}, actual={actual}."
        )
    }