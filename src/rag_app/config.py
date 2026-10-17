from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    chroma_persist_directory: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "data/chroma")
    collection_name: str = os.getenv("COLLECTION_NAME", "rag_document_qa")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    top_k: int = int(os.getenv("TOP_K", "4"))


settings = Settings()


def get_settings() -> Settings:
    return settings


def ensure_directories() -> None:
    Path(settings.chroma_persist_directory).mkdir(parents=True, exist_ok=True)
