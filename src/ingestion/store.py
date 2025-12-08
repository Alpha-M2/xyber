"""Document ingestion pipeline."""

from pathlib import Path
from typing import Dict, List

import chromadb

from src.config import settings
from src.utils.logger import setup_logger
from src.utils.text_processor import chunk_text, clean_text

logger = setup_logger(__name__)


class DocumentStore:
    """Manages document storage and retrieval with ChromaDB."""

    def __init__(self, persist_dir: str = None):
        """Initialize ChromaDB client."""
        # Use configured chroma path
        self.persist_dir = persist_dir or str(settings.chroma_db_path)

        # Create persist directory
        Path(self.persist_dir).mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(path=self.persist_dir)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="xyber_docs", metadata={"hnsw:space": "cosine"}
        )

        logger.info(f"DocumentStore initialized at {self.persist_dir}")

    def ingest_documents(self, documents: Dict[str, str]) -> int:
        """Ingest documents into the vector store.

        Args:
            documents: Dict of {url: content}

        Returns:
            Number of chunks ingested
        """
        logger.info(f"Starting ingestion of {len(documents)} documents")

        chunks_added = 0

        for doc_id, content in documents.items():
            # Clean content
            content = clean_text(content)

            # Split into chunks
            doc_chunks = chunk_text(
                content, chunk_size=settings.chunk_size, overlap=settings.chunk_overlap
            )

            # Add chunks to collection
            for i, chunk in enumerate(doc_chunks):
                if not chunk or len(chunk.strip()) < 50:
                    continue

                chunk_id = f"{doc_id}#{i}"

                try:
                    self.collection.add(
                        documents=[chunk],
                        metadatas=[{"source": doc_id, "chunk_index": i}],
                        ids=[chunk_id],
                    )
                    chunks_added += 1
                except Exception as e:
                    logger.error(f"Error adding chunk {chunk_id}: {str(e)}")

        logger.info(f"Ingestion complete. Added {chunks_added} chunks")
        return chunks_added

    def search(self, query: str, k: int = None) -> List[Dict]:
        """Search for relevant documents.

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of relevant documents with metadata
        """
        k = k or settings.retrieve_k

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=k,
                include=["documents", "metadatas", "distances"],
            )

            # Format results
            formatted = []
            if results and results["documents"]:
                for doc, meta, distance in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                ):
                    formatted.append(
                        {
                            "content": doc,
                            "source": meta.get("source", "unknown"),
                            "chunk_index": meta.get("chunk_index", 0),
                            "distance": distance,
                        }
                    )

            return formatted

        except Exception as e:
            logger.error(f"Error searching: {str(e)}")
            return []

    def get_stats(self) -> Dict:
        """Get collection statistics."""
        try:
            count = self.collection.count()
            return {"total_chunks": count, "collection_name": "xyber_docs"}
        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            return {"total_chunks": 0, "collection_name": "xyber_docs"}

    # Only ingest_documents and search are needed for core functionality
