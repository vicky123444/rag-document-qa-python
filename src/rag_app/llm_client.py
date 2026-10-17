from __future__ import annotations

from openai import OpenAI

from .config import settings


class LLMClient:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        key = api_key or settings.openai_api_key
        if not key:
            raise ValueError("OPENAI_API_KEY is required for answer generation. Configure it in .env.")
        self.client = OpenAI(api_key=key)
        self.model = model or settings.openai_model

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(model=self.model, input=prompt)
        return response.output_text
