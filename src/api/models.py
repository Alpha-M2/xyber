"""Pydantic models for API requests and responses."""

from typing import List, Optional

from pydantic import BaseModel


class QueryRequest(BaseModel):
    """Query request model."""

    question: str
    k: Optional[int] = None


class QueryResponse(BaseModel):
    """Query response model."""

    answer: str
    sources: List[str]
    retrieved_chunks: int
    has_answer: bool
    error: Optional[str] = None


## Only QueryRequest and QueryResponse are needed for core functionality
