from __future__ import annotations

from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings

from .config import settings


class VectorStore:
    def __init__(self, persist_directory: str | None = None, collection_name: str | None = None):
        self.persist_directory = persist_directory or settings.chroma_persist_directory
        self.collection_name = collection_name or settings.collection_name
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def add_documents(self, documents: list[dict[str, Any]]) -> None:
        if not documents:
            return
        self.collection.add(
            ids=[doc["id"] for doc in documents],
            embeddings=[doc["embedding"] for doc in documents],
            documents=[doc["text"] for doc in documents],
            metadatas=[doc["metadata"] for doc in documents],
        )

    def query(self, query_embedding: list[float], top_k: int = 4) -> list[dict[str, Any]]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        docs: list[dict[str, Any]] = []
        for i, text in enumerate(results["documents"][0]):
            docs.append(
                {
                    "text": text,
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i],
                }
            )
        return docs

    def reset(self) -> None:
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
