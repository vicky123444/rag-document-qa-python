from rag_app.rag_pipeline import RAGPipeline


class FakeEmbeddingClient:
    def embed_text(self, text):
        return [0.1, 0.2, 0.3]

    def embed_batch(self, texts):
        return [[0.1, 0.2, 0.3] for _ in texts]


class FakeLLMClient:
    def generate(self, prompt):
        assert "Context:" in prompt
        return "Start by checking the pod events and logs."


class FakeVectorStore:
    def query(self, query_embedding, top_k=4):
        return [
            {
                "text": "Check pod events and container logs when the pod is in CrashLoopBackOff.",
                "metadata": {"source": "eks-troubleshooting.md", "page_number": 2},
                "distance": 0.15,
            }
        ]

    def add_documents(self, documents):
        self.documents = documents


def test_rag_pipeline_answer_question_returns_sources_and_answer():
    pipeline = RAGPipeline(
        vector_store=FakeVectorStore(),
        embedding_client=FakeEmbeddingClient(),
        llm_client=FakeLLMClient(),
        top_k=1,
    )

    result = pipeline.answer_question("How do I investigate a pod in CrashLoopBackOff?")

    assert result["question"] == "How do I investigate a pod in CrashLoopBackOff?"
    assert "pod" in result["answer"]
    assert result["sources"] == ["eks-troubleshooting.md"]
    assert result["chunks"][0].source == "eks-troubleshooting.md"


def test_rag_pipeline_rejects_empty_question():
    pipeline = RAGPipeline(
        vector_store=FakeVectorStore(),
        embedding_client=FakeEmbeddingClient(),
        llm_client=FakeLLMClient(),
        top_k=1,
    )

    try:
        pipeline.answer_question("   ")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "empty" in str(exc).lower()
