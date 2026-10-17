from rag_app import document_loader


class FakePage:
    def __init__(self, text):
        self.text = text

    def extract_text(self):
        return self.text


class FakePdfReader:
    def __init__(self, _path):
        self.pages = [
            FakePage("Page one text"),
            FakePage("   "),
            FakePage("Page three text"),
        ]


def test_pdf_documents_keep_page_numbers_and_skip_empty_pages(tmp_path, monkeypatch):
    pdf_path = tmp_path / "guide.pdf"
    pdf_path.write_bytes(b"fake pdf")
    monkeypatch.setattr(document_loader, "PdfReader", FakePdfReader)

    documents = list(document_loader.iter_documents(tmp_path))

    assert [(doc.content, doc.source, doc.page_number) for doc in documents] == [
        ("Page one text", "guide.pdf", 1),
        ("Page three text", "guide.pdf", 3),
    ]
