from rag_app.retriever import RetrievedChunk, format_retrieval_results


def test_format_retrieval_results_maps_metadata():
    results = [
        {
            "text": "some relevant text",
            "metadata": {"source": "eks-troubleshooting.md", "page_number": 3},
            "distance": 0.23,
        }
    ]

    retrieved = format_retrieval_results(results)

    assert len(retrieved) == 1
    assert isinstance(retrieved[0], RetrievedChunk)
    assert retrieved[0].source == "eks-troubleshooting.md"
    assert retrieved[0].page_number == 3
    assert retrieved[0].distance == 0.23
