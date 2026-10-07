from src.data.loader import load_text


def test_load_text():
    text = load_text(
        "test_data/sample_report.txt"
    )

    print("TEXT LOADED")
    print("-----------")
    print(text)


test_load_text()