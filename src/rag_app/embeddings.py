from __future__ import annotations

from openai import OpenAI

from .config import settings


class EmbeddingClient:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        key = api_key or settings.openai_api_key
        if not key:
            raise ValueError("OPENAI_API_KEY is required for embeddings. Configure it in .env.")
        self.client = OpenAI(api_key=key)
        self.model = model or settings.embedding_model

    def embed_text(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Cannot embed empty text")
        response = self.client.embeddings.create(model=self.model, input=text)
        return response.data[0].embedding

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        response = self.client.embeddings.create(model=self.model, input=texts)
        return [item.embedding for item in response.data]
