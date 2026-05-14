"""RAG pipeline skeleton for financial and supply chain documents.

Flow:
    PDF -> text chunks -> embeddings -> ChromaDB -> retrieved context -> LLM answer.

This first phase defines the interface. Later phases will fill in ingestion,
retrieval, citations, and answer generation.
"""

from dataclasses import dataclass


@dataclass
class RetrievedChunk:
    """A document passage returned by semantic search."""

    text: str
    source: str
    page: int | None = None
    score: float | None = None


class RagPipeline:
    """Coordinates document ingestion and semantic retrieval."""

    def ingest_pdf(self, file_path: str, document_name: str) -> None:
        """Add a PDF to the vector database. Implemented in Phase 5."""

        raise NotImplementedError("PDF ingestion will be implemented in the RAG phase.")

    def retrieve(self, question: str, top_k: int = 5) -> list[RetrievedChunk]:
        """Find relevant document chunks for a user question."""

        raise NotImplementedError("Semantic retrieval will be implemented in the RAG phase.")
