import pandas as pd

from src.data.quality import analyze_data_quality


def main():
    df = pd.DataFrame({
        "Mixed": [
            20,
            "21",
            "unknown",
            None,
        ],
        "Name": [
            "Alice",
            "Bob",
            "Charlie",
            None,
        ],
        "EmptyColumn": [
            None,
            None,
            None,
            None,
        ],
    })

    report = analyze_data_quality(df)

    print("TYPE ISSUES")
    print(report["type_issues"])

    print("\nEMPTY ROWS")
    print(report["empty_rows"])

    print("\nEMPTY COLUMNS")
    print(report["empty_columns"])

    print("\nORIGINAL DATA")
    print(df)


if __name__ == "__main__":
    main()