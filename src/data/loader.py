from pathlib import Path
import pandas as pd


def load_table(file_path: str | Path) -> pd.DataFrame:
    """
    Load a CSV or Excel file into a Pandas DataFrame.

    The original data is not modified.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = file_path.suffix.lower()

    if extension == ".csv":
        return pd.read_csv(file_path)

    if extension in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}. "
        "Only CSV and Excel files are supported."
    )

def load_tables(file_paths: list[str | Path]) -> dict[str, pd.DataFrame]:
    """
    Load multiple CSV or Excel files.

    Returns a dictionary where:
        key   = table name
        value = Pandas DataFrame
    """

    tables = {}

    for file_path in file_paths:
        file_path = Path(file_path)

        table_name = file_path.stem

        tables[table_name] = load_table(file_path)

    return tables