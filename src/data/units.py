import re
import pandas as pd


UNIT_PATTERNS = {
    "kg": [r"\bkg\b", r"\bkilograms?\b"],
    "g": [r"\bg\b", r"\bgrams?\b"],
    "mg": [r"\bmg\b", r"\bmilligrams?\b"],
    "km": [r"\bkm\b", r"\bkilometers?\b"],
    "m": [r"\bm\b", r"\bmeters?\b"],
    "cm": [r"\bcm\b", r"\bcentimeters?\b"],
    "L": [r"\bL\b", r"\bliters?\b", r"\blitres?\b"],
    "mL": [r"\bmL\b", r"\bmilliliters?\b", r"\bmillilitres?\b"],
    "%": [r"%", r"\bpercent\b"],
}


def detect_units(df: pd.DataFrame) -> dict:
    """
    Detect explicit measurement units in text-like columns.

    Returns detected units for each column.

    This function does not modify the DataFrame.
    """

    detected = {}

    for column in df.columns:

        # Numeric columns do not contain explicit unit information
        if pd.api.types.is_numeric_dtype(df[column]):
            continue

        units = set()

        for value in df[column].dropna():

            value = str(value)

            for unit, patterns in UNIT_PATTERNS.items():

                for pattern in patterns:

                    if re.search(pattern, value):
                        units.add(unit)

        if units:
            detected[column] = sorted(units)

    return detected