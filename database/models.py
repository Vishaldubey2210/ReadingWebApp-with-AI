"""
==========================================================
ReadingAI Database Models
==========================================================
"""

from dataclasses import dataclass


# ==========================================================
# STUDENT
# ==========================================================

@dataclass
class Student:

    name: str

    age: int = 0

    standard: str = ""

    school: str = ""


# ==========================================================
# ARTICLE
# ==========================================================

@dataclass
class Article:

    name: str

    level: str

    total_words: int

    total_sentences: int


# ==========================================================
# READING RESULT
# ==========================================================

@dataclass
class ReadingResult:

    student_name: str

    article_name: str

    accuracy: float

    fluency: float

    pronunciation: float

    wpm: float

    score: float

    total_words: int

    correct_words: int

    wrong_words: int

    attempts: int


# ==========================================================
# SESSION
# ==========================================================

@dataclass
class ReadingSessionModel:

    article: str = ""

    current_word: str = ""

    current_index: int = 0

    completed: bool = False

    attempts: int = 0

    accuracy: float = 0

    fluency: float = 0

    pronunciation: float = 0

    score: float = 0

    wpm: float = 0


# ==========================================================
# WORD RESULT
# ==========================================================

@dataclass
class WordResult:

    expected: str

    spoken: str

    similarity: float

    correct: bool

    attempts: int


# ==========================================================
# PRONUNCIATION
# ==========================================================

@dataclass
class PronunciationResult:

    word: str

    score: float

    confidence: float

    accepted: bool

    stars: int

    level: str


# ==========================================================
# HINT
# ==========================================================

@dataclass
class HintModel:

    word: str

    syllables: list

    hindi: str

    show: bool