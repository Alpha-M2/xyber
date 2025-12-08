"""FastAPI backend server."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.models import QueryRequest
from src.config import settings
from src.core.rag import RAGPipeline
from src.ingestion.crawler import crawl_xyber_docs
from src.ingestion.store import DocumentStore
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(
    title="Xyber Documentation RAG Chatbot",
    description="RAG-based chatbot with Telegram integration",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
document_store: DocumentStore = None
rag_pipeline: RAGPipeline = None


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global document_store, rag_pipeline

    try:
        document_store = DocumentStore()
        rag_pipeline = RAGPipeline(document_store)
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing services: {str(e)}")
        raise


@app.get("/health")
async def health_check():
    if document_store is None:
        raise HTTPException(status_code=503, detail="Document store not initialized")
    return {"status": "healthy"}


## Removed /stats endpoint for minimal API


@app.post("/ingest")
async def ingest_documents():
    if document_store is None:
        raise HTTPException(status_code=503, detail="Document store not initialized")
    docs = await crawl_xyber_docs(
        url=settings.xyber_docs_url, max_depth=settings.max_crawl_depth
    )
    chunks = document_store.ingest_documents(docs)
    return {"success": True, "chunks_ingested": chunks}


@app.post("/query")
async def query(request: QueryRequest):
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    result = await rag_pipeline.query(request.question, k=request.k)
    return result


@app.get("/")
async def root():
    """Serve the web UI."""
    web_dir = Path(__file__).parent.parent / "web"
    index_path = web_dir / "index.html"

    if not index_path.exists():
        logger.warning("index.html not found at %s", index_path)
        return {"message": "Web UI not configured"}

    with open(index_path) as f:
        return f.read()


def run_server():
    """Run the FastAPI server."""
    import uvicorn

    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    run_server()
