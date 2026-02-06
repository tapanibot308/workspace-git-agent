"""
Book Outliner - Generates book outlines from research sources.
"""

import os
import re
import json
import logging
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from datetime import datetime

# Try to import Source from research.models, create fallback if not available
try:
    from research.models import Source
except ImportError:
    @dataclass
    class Source:
        """Fallback Source dataclass when research.models is not available."""
        url: str
        title: Optional[str] = None
        content: Optional[str] = None
        snippet: Optional[str] = None
        source_type: str = "web"
        relevance_score: float = 0.0

# Try to import httpx, create fallback if not available
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    # Create a mock httpx for type hints
    class MockHttpx:
        class AsyncClient:
            pass
        class TimeoutException(Exception):
            pass
        class HTTPStatusError(Exception):
            pass
    httpx = MockHttpx()


# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class Chapter:
    """Represents a chapter in the book outline."""
    title: str
    word_budget: int
    key_points: List[str] = field(default_factory=list)
    description: str = ""
    order: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert chapter to dictionary."""
        return {
            "title": self.title,
            "word_budget": self.word_budget,
            "key_points": self.key_points,
            "description": self.description,
            "order": self.order
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Chapter":
        """Create chapter from dictionary."""
        return cls(
            title=data.get("title", ""),
            word_budget=data.get("word_budget", 1000),
            key_points=data.get("key_points", []),
            description=data.get("description", ""),
            order=data.get("order", 0)
        )


@dataclass
class BookOutline:
    """Represents a complete book outline."""
    title: str
    chapters: List[Chapter] = field(default_factory=list)
    themes: List[str] = field(default_factory=list)
    tone_description: str = ""
    plot_hypothesis: str = ""
    total_word_count: int = 0
    target_length: int = 50000
    genre: str = "non-fiction"
    references: List[Source] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert outline to dictionary."""
        return {
            "title": self.title,
            "chapters": [ch.to_dict() for ch in self.chapters],
            "themes": self.themes,
            "tone_description": self.tone_description,
            "plot_hypothesis": self.plot_hypothesis,
            "total_word_count": self.total_word_count,
            "target_length": self.target_length,
            "genre": self.genre,
            "references": [
                {"url": r.url, "title": r.title, "source_type": r.source_type}
                for r in self.references
            ],
            "generated_at": self.generated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BookOutline":
        """Create outline from dictionary."""
        chapters = [Chapter.from_dict(ch) for ch in data.get("chapters", [])]
        references = [
            Source(
                url=r.get("url", ""),
                title=r.get("title"),
                source_type=r.get("source_type", "web")
            )
            for r in data.get("references", [])
        ]
        return cls(
            title=data.get("title", ""),
            chapters=chapters,
            themes=data.get("themes", []),
            tone_description=data.get("tone_description", ""),
            plot_hypothesis=data.get("plot_hypothesis", ""),
            total_word_count=data.get("total_word_count", 0),
            target_length=data.get("target_length", 50000),
            genre=data.get("genre", "non-fiction"),
            references=references,
            generated_at=data.get("generated_at", datetime.now().isoformat())
        )


class BookOutliner:
    """Generates book outlines using LLM and research sources."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the outliner with optional API key."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        self.model = os.getenv("LLM_MODEL", "gpt-4")
        self.max_retries = 3
        self.timeout = 60.0
        
        if not HTTPX_AVAILABLE:
            logger.warning("httpx not available, LLM calls will fail")

    def generate_outline(
        self,
        title: str,
        sources: List[Source],
        target_length: int = 50000,
        genre: str = "non-fiction",
        themes: Optional[List[str]] = None
    ) -> BookOutline:
        """
        Generate a book outline from research sources.
        
        Args:
            title: Book title
            sources: List of research sources
            target_length: Target word count
            genre: Book genre
            themes: Optional list of themes to focus on
            
        Returns:
            BookOutline object
        """
        logger.info(f"Generating outline for '{title}' with {len(sources)} sources")
        
        # Create prompt for LLM
        prompt = self._create_outline_prompt(
            title=title,
            sources=sources,
            target_length=target_length,
            genre=genre,
            themes=themes or []
        )
        
        # Call LLM with retry
        response = self._call_llm_with_retry(prompt)
        
        # Parse response
        outline_data = self._parse_json_response(response)
        
        # Validate and create outline
        outline = self._validate_and_create_outline(
            data=outline_data,
            title=title,
            sources=sources,
            target_length=target_length,
            genre=genre
        )
        
        logger.info(f"Generated outline with {len(outline.chapters)} chapters")
        return outline

    def _create_outline_prompt(
        self,
        title: str,
        sources: List[Source],
        target_length: int,
        genre: str,
        themes: List[str]
    ) -> str:
        """Create a prompt for the LLM to generate an outline."""
        # Estimate chapter count
        chapter_count = self._estimate_chapter_count(target_length)
        
        # Build sources summary
        sources_text = ""
        for i, src in enumerate(sources[:10], 1):  # Limit to 10 sources
            content = src.content or src.snippet or ""
            sources_text += f"\nSource {i}: {src.title or src.url}\n"
            sources_text += f"Content: {content[:500]}...\n"
        
        themes_text = ", ".join(themes) if themes else "To be determined from sources"
        
        prompt = f"""You are an expert book outliner and editor. Create a detailed book outline based on the following research sources.

BOOK TITLE: {title}
TARGET LENGTH: {target_length} words
GENRE: {genre}
THEMES: {themes_text}
NUMBER OF CHAPTERS: Approximately {chapter_count}

RESEARCH SOURCES:
{sources_text}

Create a JSON response with this exact structure:
{{
    "chapters": [
        {{
            "title": "Chapter title",
            "word_budget": integer_word_count,
            "key_points": ["point 1", "point 2", "point 3"],
            "description": "Detailed description of chapter content",
            "order": chapter_number
        }}
    ],
    "themes": ["theme1", "theme2", "theme3"],
    "tone_description": "Description of the book's tone and style",
    "plot_hypothesis": "For fiction: main plot arc. For non-fiction: core thesis/argument"
}}

Requirements:
- Total word budget across all chapters should approximately equal {target_length}
- Each chapter must have a clear focus
- Key points should be specific and actionable
- Order chapters logically (introduction to conclusion)
- For non-fiction: ensure logical flow of arguments
- For fiction: ensure proper story arc structure

Respond ONLY with the JSON object, no additional text."""
        
        return prompt

    def _estimate_chapter_count(self, target_length: int) -> int:
        """Estimate the number of chapters based on target word count."""
        # Average chapter length: 3000-5000 words for non-fiction
        avg_chapter_length = 4000
        estimated = max(3, target_length // avg_chapter_length)
        return min(estimated, 30)  # Cap at 30 chapters

    def _call_llm_with_retry(self, prompt: str) -> str:
        """Call LLM API with retry logic."""
        if not HTTPX_AVAILABLE:
            raise RuntimeError("httpx is required for LLM calls")
        
        if not self.api_key:
            raise ValueError("API key not provided")
        
        last_error = None
        
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.debug(f"LLM call attempt {attempt}")
                
                import asyncio
                
                async def _call():
                    async with httpx.AsyncClient(timeout=self.timeout) as client:
                        response = await client.post(
                            f"{self.base_url}/chat/completions",
                            headers={
                                "Authorization": f"Bearer {self.api_key}",
                                "Content-Type": "application/json"
                            },
                            json={
                                "model": self.model,
                                "messages": [
                                    {"role": "system", "content": "You are a helpful book outlining assistant."},
                                    {"role": "user", "content": prompt}
                                ],
                                "temperature": 0.7,
                                "max_tokens": 4000
                            }
                        )
                        response.raise_for_status()
                        data = response.json()
                        return data["choices"][0]["message"]["content"]
                
                return asyncio.run(_call())
                
            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt} failed: {e}")
                if attempt < self.max_retries:
                    import time
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        raise RuntimeError(f"LLM call failed after {self.max_retries} attempts: {last_error}")

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from LLM response with fallback strategies."""
        # Try direct JSON parse
        try:
            return json.loads(response.strip())
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from markdown code blocks
        patterns = [
            r'```json\s*(.*?)\s*```',  # ```json ... ```
            r'```\s*(.*?)\s*```',      # ``` ... ```
            r'\{.*\}',                  # Raw JSON object
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response, re.DOTALL)
            for match in matches:
                try:
                    return json.loads(match.strip())
                except json.JSONDecodeError:
                    continue
        
        # Fallback: try to fix common JSON issues
        cleaned = response.strip()
        cleaned = re.sub(r'^[^{]*', '', cleaned)  # Remove leading non-JSON
        cleaned = re.sub(r'[^}]*$', '', cleaned)  # Remove trailing non-JSON
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response was: {response[:500]}")
            raise ValueError(f"Could not parse LLM response as JSON: {e}")

    def _validate_and_create_outline(
        self,
        data: Dict[str, Any],
        title: str,
        sources: List[Source],
        target_length: int,
        genre: str
    ) -> BookOutline:
        """Validate parsed data and create BookOutline object."""
        chapters_data = data.get("chapters", [])
        if not chapters_data:
            raise ValueError("No chapters found in LLM response")
        
        chapters = []
        total_word_budget = 0
        
        for i, ch_data in enumerate(chapters_data):
            # Ensure required fields
            ch_title = ch_data.get("title", f"Chapter {i+1}")
            ch_budget = ch_data.get("word_budget", target_length // len(chapters_data))
            ch_points = ch_data.get("key_points", [])
            ch_desc = ch_data.get("description", "")
            
            chapter = Chapter(
                title=ch_title,
                word_budget=ch_budget,
                key_points=ch_points if isinstance(ch_points, list) else [ch_points],
                description=ch_desc,
                order=ch_data.get("order", i + 1)
            )
            chapters.append(chapter)
            total_word_budget += ch_budget
        
        # Sort by order
        chapters.sort(key=lambda c: c.order)
        
        outline = BookOutline(
            title=title,
            chapters=chapters,
            themes=data.get("themes", []),
            tone_description=data.get("tone_description", ""),
            plot_hypothesis=data.get("plot_hypothesis", ""),
            total_word_count=total_word_budget,
            target_length=target_length,
            genre=genre,
            references=sources,
            generated_at=datetime.now().isoformat()
        )
        
        return outline

    def generate_outline_legacy(
        self,
        title: str,
        source_texts: List[str],
        target_length: int = 50000
    ) -> Dict[str, Any]:
        """
        Legacy compatibility method for simpler outline generation.
        
        Args:
            title: Book title
            source_texts: List of source text strings
            target_length: Target word count
            
        Returns:
            Dictionary with outline data
        """
        # Convert strings to Source objects
        sources = [
            Source(url=f"legacy://{i}", content=text, source_type="legacy")
            for i, text in enumerate(source_texts)
        ]
        
        outline = self.generate_outline(
            title=title,
            sources=sources,
            target_length=target_length
        )
        
        return outline.to_dict()


# Convenience function for direct usage
def create_outline(
    title: str,
    sources: List[Source],
    api_key: Optional[str] = None,
    **kwargs
) -> BookOutline:
    """Convenience function to create an outline."""
    outliner = BookOutliner(api_key=api_key)
    return outliner.generate_outline(title=title, sources=sources, **kwargs)


if __name__ == "__main__":
    # Simple test
    logging.basicConfig(level=logging.INFO)
    
    # Test imports work
    print("Testing imports...")
    print(f"Source class: {Source}")
    print(f"Chapter class: {Chapter}")
    print(f"BookOutline class: {BookOutline}")
    print(f"BookOutliner class: {BookOutliner}")
    print("All classes imported successfully!")
