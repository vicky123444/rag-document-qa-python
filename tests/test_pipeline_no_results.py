from rag_app.rag_pipeline import RAGPipeline


class FakeEmbeddingClient:
    def embed_text(self, text):
        return [0.0, 0.0, 0.0]


class EmptyVectorStore:
    def query(self, query_embedding, top_k=4):
        return []


class FakeLLMClient:
    def generate(self, prompt):
        raise AssertionError("LLM must not be called when nothing was retrieved")


def test_empty_retrieval_returns_fallback_without_calling_llm():
    pipeline = RAGPipeline(
        vector_store=EmptyVectorStore(),
        embedding_client=FakeEmbeddingClient(),
        llm_client=FakeLLMClient(),
        top_k=2,
    )

    result = pipeline.answer_question("Question not covered by docs")

    assert result["sources"] == []
    assert result["chunks"] == []
    assert "could not find relevant information" in result["answer"].lower()
