from src.data.loader import load_pdf


def test_load_pdf():
    text = load_pdf(
        "test_data/sample_report.pdf"
    )

    print("PDF LOADED")
    print("----------")
    print(text)


def test_load_multipage_pdf():
    text = load_pdf(
        "test_data/multipage_report.pdf"
    )

    print("MULTI-PAGE PDF LOADED")
    print("---------------------")
    print(text)


def test_scanned_pdf_rejected():
    try:
        load_pdf(
            "test_data/scanned_report.pdf"
        )
    except ValueError as error:
        print("SCANNED PDF HANDLED")
        print("-------------------")
        print(error)
    else:
        raise AssertionError(
            "Scanned PDF should have raised ValueError"
        )


test_load_pdf()
test_load_multipage_pdf()
test_scanned_pdf_rejected()