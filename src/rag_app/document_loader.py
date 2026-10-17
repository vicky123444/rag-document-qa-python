from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader


@dataclass
class Document:
    content: str
    source: str
    page_number: int | None = None


def load_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def iter_documents(source_dir: str | Path) -> Iterable[Document]:
    """Yield non-empty documents; PDF pages retain 1-based page numbers."""
    root = Path(source_dir)
    if not root.exists():
        raise FileNotFoundError(f"Source directory does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {root}")

    for file_path in sorted(root.iterdir()):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() == ".pdf":
            reader = PdfReader(str(file_path))
            for page_number, page in enumerate(reader.pages, start=1):
                content = page.extract_text() or ""
                if content.strip():
                    yield Document(content=content, source=file_path.name, page_number=page_number)
        elif file_path.suffix.lower() in {".txt", ".md", ".markdown"}:
            content = load_text_file(file_path)
            if content.strip():
                yield Document(content=content, source=file_path.name)
