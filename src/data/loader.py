from pathlib import Path
import pandas as pd


def load_text(file_path: str | Path) -> str:
    """
    Load a TXT file and return its text content.

    The original file is not modified.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if file_path.suffix.lower() != ".txt":
        raise ValueError(
            f"Unsupported file type: {file_path.suffix}. "
            "Only TXT files are supported."
        )

    return file_path.read_text(
        encoding="utf-8"
    )


def load_pdf(file_path: str | Path) -> str:
    """
    Load a PDF file and return its extracted text.

    The original file is not modified.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if file_path.suffix.lower() != ".pdf":
        raise ValueError(
            f"Unsupported file type: {file_path.suffix}. "
            "Only PDF files are supported."
        )

    from pypdf import PdfReader

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    extracted_text = "\n".join(pages).strip()

    if not extracted_text:
        raise ValueError(
            "PDF contains no extractable text. "
            "It may be a scanned or image-only PDF and requires OCR."
        )

    return extracted_text


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