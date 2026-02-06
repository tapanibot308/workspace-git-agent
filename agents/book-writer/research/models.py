"""
Research models for book writing pipeline.
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class Source:
    """Represents a research source."""
    url: str
    title: Optional[str] = None
    content: Optional[str] = None
    snippet: Optional[str] = None
    source_type: str = "web"
    relevance_score: float = 0.0
