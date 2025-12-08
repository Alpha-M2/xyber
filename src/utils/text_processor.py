"""Text processing utilities."""

import re
from typing import List


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)
    # Remove special characters but keep punctuation
    text = re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]", "", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

        # Avoid infinite loop on very small texts
        if overlap >= chunk_size:
            break

    return chunks


## Only clean_text and chunk_text are needed for core functionality
