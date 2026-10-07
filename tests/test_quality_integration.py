from src.data.loader import load_table
from src.data.quality import analyze_data_quality


def main():
    file_path = "test_data/messy_sales.csv"

    df = load_table(file_path)

    print("LOADED DATA")
    print(df)

    print("\n" + "=" * 60)

    report = analyze_data_quality(df)

    print("DATA QUALITY REPORT")
    print("--------------------")

    print("\nMissing values:")
    print(report["missing_values"])

    print("\nDuplicates:")
    print(report["duplicates"])

    print("\nOutliers:")
    print(report["outliers"])

    print("\nType issues:")
    print(report["type_issues"])

    print("\nInconsistencies:")
    print(report["inconsistencies"])

    print("\nSummary:")
    print(report["summary"])


if __name__ == "__main__":
    main()