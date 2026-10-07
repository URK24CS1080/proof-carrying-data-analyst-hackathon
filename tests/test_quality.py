import pandas as pd

from src.data.quality import analyze_data_quality


def main():
    df = pd.DataFrame({
        "Name": [
            "Alice",
            "Bob",
            "bob",
            "Charlie",
            "Alice",
            None,
            "Eve"
        ],
        "Age": [
            20,
            21,
            21,
            22,
            20,
            None,
            200
        ],
        "Status": [
            "Active",
            "active ",
            "Active",
            "Inactive",
            "Active",
            "NULL",
            ""
        ],
        "Country": [
          "India",
          "India",
          "India",
          "India",
          "India",
          "India",
          "India"
        ]
    })

    print("ORIGINAL DATA")
    print(df)
    print("\n" + "=" * 50)

    report = analyze_data_quality(df)

    print("MISSING VALUES")
    print(report["missing_values"])

    print("\nNULL-LIKE VALUES")
    print(report["null_values"])

    print("\nDUPLICATES")
    print(report["duplicates"])

    print("\nOUTLIERS")
    print(report["outliers"])

    print("\nTYPE ISSUES")
    print(report["type_issues"])

    print("\nCATEGORICAL INCONSISTENCIES")
    print(report["inconsistencies"])

    print("\nEMPTY ROWS")
    print(report["empty_rows"])

    print("\nEMPTY COLUMNS")
    print(report["empty_columns"])

    print("\nCONSTANT COLUMNS")
    print(report["constant_columns"])
    print("\nCHECKING ORIGINAL DATA WAS NOT MODIFIED")
    print(df)


if __name__ == "__main__":
    main()