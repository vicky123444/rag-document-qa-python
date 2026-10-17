from __future__ import annotations

import uuid
from typing import Any

from .chunker import chunk_text
from .config import settings
from .document_loader import iter_documents
from .embeddings import EmbeddingClient
from .prompt_builder import build_grounded_prompt
from .retriever import format_retrieval_results
from .vector_store import VectorStore


class RAGPipeline:
    def __init__(
        self,
        vector_store: VectorStore | None = None,
        embedding_client: EmbeddingClient | None = None,
        llm_client: Any | None = None,
        top_k: int | None = None,
    ) -> None:
        self.vector_store = vector_store or VectorStore()
        self.embedding_client = embedding_client or EmbeddingClient()
        self.llm_client = llm_client
        self.top_k = settings.top_k if top_k is None else top_k
        if self.top_k <= 0:
            raise ValueError("top_k must be greater than 0")

    def ingest_documents(self, source_dir: str) -> list[str]:
        documents = list(iter_documents(source_dir))
        chunk_records: list[dict[str, Any]] = []
        for document in documents:
            chunks = chunk_text(
                document.content,
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
                source=document.source,
                page_number=document.page_number,
            )
            if not chunks:
                continue
            embeddings = self.embedding_client.embed_batch([chunk.text for chunk in chunks])
            if len(embeddings) != len(chunks):
                raise RuntimeError("Embedding provider returned a different number of vectors than input chunks")
            for chunk, embedding in zip(chunks, embeddings):
                metadata = {"source": chunk.source, "chunk_index": chunk.chunk_index}
                if chunk.page_number is not None:
                    metadata["page_number"] = chunk.page_number
                chunk_records.append(
                    {
                        "id": str(uuid.uuid4()),
                        "text": chunk.text,
                        "embedding": embedding,
                        "metadata": metadata,
                    }
                )
        self.vector_store.add_documents(chunk_records)
        return [record["metadata"]["source"] for record in chunk_records]

    def answer_question(self, question: str) -> dict[str, Any]:
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
        if self.llm_client is None:
            raise ValueError("A language model client is required to answer questions")

        query_embedding = self.embedding_client.embed_text(question)
        results = self.vector_store.query(query_embedding=query_embedding, top_k=self.top_k)
        retrieved = format_retrieval_results(results)
        if not retrieved:
            return {
                "question": question,
                "answer": "I could not find relevant information in the indexed documents.",
                "sources": [],
                "chunks": [],
            }
        prompt = build_grounded_prompt(question.strip(), retrieved)
        answer = self.llm_client.generate(prompt)
        return {
            "question": question,
            "answer": answer,
            "sources": sorted({chunk.source for chunk in retrieved}),
            "chunks": retrieved,
        }
