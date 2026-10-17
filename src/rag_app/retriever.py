from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class RetrievedChunk:
    text: str
    source: str
    page_number: int | None = None
    distance: float | None = None


def format_retrieval_results(results: list[dict[str, Any]]) -> list[RetrievedChunk]:
    retrieved: list[RetrievedChunk] = []
    for item in results:
        metadata = item.get("metadata", {})
        retrieved.append(
            RetrievedChunk(
                text=item.get("text", ""),
                source=metadata.get("source", "unknown"),
                page_number=metadata.get("page_number"),
                distance=item.get("distance"),
            )
        )
    return retrieved
