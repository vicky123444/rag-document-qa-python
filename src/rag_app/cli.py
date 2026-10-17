from __future__ import annotations

import argparse
import sys

from .config import ensure_directories
from .embeddings import EmbeddingClient
from .llm_client import LLMClient
from .rag_pipeline import RAGPipeline
from .vector_store import VectorStore


def ingest_command(source: str) -> None:
    ensure_directories()
    pipeline = RAGPipeline(vector_store=VectorStore(), embedding_client=EmbeddingClient(), llm_client=None)
    sources = pipeline.ingest_documents(source)
    print(f"Indexed {len(sources)} chunks from {source}")


def ask_command(question: str) -> None:
    ensure_directories()
    pipeline = RAGPipeline(
        vector_store=VectorStore(),
        embedding_client=EmbeddingClient(),
        llm_client=LLMClient(),
    )
    result = pipeline.answer_question(question)
    print(f"Question:\n{result['question']}\n")
    print(f"Answer:\n{result['answer']}\n")
    if result["sources"]:
        print("Retrieved sources:")
        for source in result["sources"]:
            print(f"- {source}")
    else:
        print("No source passages were retrieved.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Document QA assistant powered by RAG")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="Index documents in a directory")
    ingest_parser.add_argument("--source", required=True, help="Directory containing TXT, MD, or PDF files")
    ingest_parser.set_defaults(func=lambda args: ingest_command(args.source))

    ask_parser = subparsers.add_parser("ask", help="Ask a question about the indexed content")
    ask_parser.add_argument("question", help="Question to answer")
    ask_parser.set_defaults(func=lambda args: ask_command(args.question))
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
