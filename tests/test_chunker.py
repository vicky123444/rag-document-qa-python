from rag_app.chunker import chunk_text


def test_chunk_text_splits_into_overlapping_chunks():
    text = " ".join([f"word{i}" for i in range(1, 51)])
    chunks = chunk_text(text, chunk_size=12, chunk_overlap=4, source="demo.txt")

    assert len(chunks) > 1
    assert chunks[0].text.startswith("word1")
    assert chunks[0].source == "demo.txt"
    assert chunks[1].text.startswith("word9")


def test_chunk_text_rejects_invalid_overlap():
    try:
        chunk_text("a b c", chunk_size=5, chunk_overlap=5)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_chunk_text_preserves_pdf_page_metadata():
    chunks = chunk_text("Page content here", chunk_size=5, chunk_overlap=1, source="guide.pdf", page_number=4)
    assert chunks[0].page_number == 4
