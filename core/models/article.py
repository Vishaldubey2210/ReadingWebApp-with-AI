"""
==========================================================
ReadingAI - Article Data Model
Author : Vishal Kumar
==========================================================
"""

from dataclasses import dataclass, field
import re
from typing import List, Dict, Any, Optional

@dataclass
class Article:
    """
    Represents an article in the ReadingAI system.
    Contains metadata, raw content, and precalculated text statistics.
    """
    id: str
    title: str
    content: str
    difficulty: str
    category: str
    language: str
    source: str
    author: str
    tags: List[str] = field(default_factory=list)
    word_count: int = 0
    sentence_count: int = 0
    estimated_reading_time_minutes: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """
        Runs automatically after initialization to calculate text statistics
        if they are not already set.
        """
        if not self.word_count or self.word_count == 0:
            self.word_count = self._calculate_word_count()
        if not self.sentence_count or self.sentence_count == 0:
            self.sentence_count = self._calculate_sentence_count()
        if not self.estimated_reading_time_minutes or self.estimated_reading_time_minutes == 0.0:
            self.estimated_reading_time_minutes = self._calculate_reading_time()

    def _calculate_word_count(self) -> int:
        """Calculates total words in the article content."""
        if not self.content:
            return 0
        return len(self.content.strip().split())

    def _calculate_sentence_count(self) -> int:
        """Calculates total sentences, supporting English and Indian language punctuation (danda)."""
        if not self.content:
            return 0
        # Split on '.', '!', '?' (English) or '।' / '|' (Hindi/Devanagari danda punctuation)
        sentences = re.split(r'[.!?।|]+', self.content)
        # Filter out empty sentences/whitespace
        return len([s for s in sentences if s.strip()])

    def _calculate_reading_time(self) -> float:
        """
        Estimates the reading time in minutes based on average reading speeds.
        Assumes average English reading speed of 200 WPM.
        """
        if self.word_count == 0:
            return 0.0
        
        # Standard average reading speeds
        # en: ~200 WPM, default/other: ~180 WPM
        wpm = 200 if self.language.lower() in ["en", "english"] else 180
        
        # Ensure we always return at least 0.1 minutes for non-empty articles
        return max(0.1, round(self.word_count / wpm, 1))

    def to_dict(self) -> Dict[str, Any]:
        """Converts the article model into a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "difficulty": self.difficulty,
            "category": self.category,
            "language": self.language,
            "source": self.source,
            "author": self.author,
            "tags": self.tags,
            "word_count": self.word_count,
            "sentence_count": self.sentence_count,
            "estimated_reading_time_minutes": self.estimated_reading_time_minutes,
            "metadata": self.metadata
        }
