"""CLI utilities for Xyber Chatbot."""

import cli

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@cli.group()
def cli():
    """Xyber Documentation RAG Chatbot CLI."""
