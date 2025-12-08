"""Configuration management for Xyber Chatbot."""

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Essential configuration
    groq_api_key: Optional[str] = None
    telegram_bot_token: Optional[str] = None
    # GROQ model id to use (set via GROQ_MODEL in .env). Update if a model is decommissioned.
    groq_model: str = "llama-3.1-8b-instant"
    xyber_docs_url: str = "https://docs.xyber.inc/"
    chroma_db_path: Path = Path("./data/chroma_db")
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieve_k: int = 5
    temperature: float = 0.3
    max_tokens: int = 2048
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    log_level: str = "INFO"
    max_crawl_depth: int = 5
    request_timeout: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


# Global settings instance
settings = Settings()
