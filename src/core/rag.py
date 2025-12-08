"""RAG pipeline using GROQ and LangChain."""

from typing import Dict, List

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

from src.config import settings
from src.ingestion.store import DocumentStore
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline."""

    def __init__(self, document_store: DocumentStore = None):
        """Initialize RAG pipeline."""
        self.document_store = document_store or DocumentStore()

        # Initialize GROQ LLM
        try:
            self.llm = ChatGroq(
                model="llama3-8b-8192",
                temperature=settings.temperature,
                max_tokens=settings.max_tokens,
                groq_api_key=settings.groq_api_key,
            )
        except Exception as e:
            logger.error(f"Error initializing GROQ: {str(e)}")
            raise

        logger.info("RAG Pipeline initialized")

    def _format_context(self, retrieved_docs: List[Dict]) -> str:
        if not retrieved_docs:
            return "No relevant documentation found."
        return "\n\n".join(doc.get("content", "") for doc in retrieved_docs)

    async def query(self, question: str, k: int = None) -> Dict:
        """Process a query through the RAG pipeline.

        Args:
            question: User's question
            k: Number of documents to retrieve

        Returns:
            Dict with answer, sources, and metadata
        """
        k = k or settings.retrieve_k

        logger.info(f"Processing query: {question}")

        # Retrieve relevant documents
        retrieved_docs = self.document_store.search(question, k=k)

        if not retrieved_docs:
            return {
                "answer": "I couldn't find any relevant information in the Xyber documentation to answer your question.",
                "sources": [],
                "retrieved_chunks": 0,
                "has_answer": False,
            }

        # Format context
        context = self._format_context(retrieved_docs)

        # Build prompt
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        try:
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            answer = response.content
            sources = list(set(doc.get("source", "") for doc in retrieved_docs))
            return {
                "answer": answer,
                "sources": sources,
                "retrieved_chunks": len(retrieved_docs),
                "has_answer": True,
            }
        except Exception as e:
            return {
                "answer": f"Error processing your question: {str(e)}",
                "sources": [],
                "retrieved_chunks": 0,
                "has_answer": False,
                "error": str(e),
            }

    # Only query method is needed for core functionality
