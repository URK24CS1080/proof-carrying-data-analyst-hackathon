import re
import pandas as pd


CURRENCY_PATTERNS = {
    "INR": [r"₹", r"\bINR\b"],
    "USD": [r"\$", r"\bUSD\b"],
    "EUR": [r"€", r"\bEUR\b"],
    "GBP": [r"£", r"\bGBP\b"],
}


def detect_currencies(df: pd.DataFrame) -> dict:
    """
    Detect obvious currency symbols or currency codes
    in string/object columns.

    Returns detected currencies for each column.

    This function does not modify the DataFrame.
    """

    detected = {}

    for column in df.columns:

        # Only inspect text-like columns
        if pd.api.types.is_numeric_dtype(df[column]):
            continue

        currencies = set()

        for value in df[column].dropna():

            value = str(value)

            for currency, patterns in CURRENCY_PATTERNS.items():

                for pattern in patterns:

                    if re.search(pattern, value):
                        currencies.add(currency)

        if currencies:
            detected[column] = sorted(currencies)

    return detected