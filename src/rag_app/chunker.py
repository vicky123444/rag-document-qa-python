from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    source: str
    page_number: int | None = None
    chunk_index: int = 0


def chunk_text(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
    source: str = "",
    page_number: int | None = None,
) -> list[Chunk]:
    """Split text into overlapping word chunks (size is measured in words)."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be non-negative")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")
    if not text.strip():
        return []

    words = text.replace("\r\n", "\n").strip().split()
    if not words:
        return []

    chunks: list[Chunk] = []
    step = chunk_size - chunk_overlap
    for index, start in enumerate(range(0, len(words), step)):
        end = min(start + chunk_size, len(words))
        chunks.append(
            Chunk(
                text=" ".join(words[start:end]),
                source=source,
                page_number=page_number,
                chunk_index=index,
            )
        )
        if end == len(words):
            break
    return chunks
