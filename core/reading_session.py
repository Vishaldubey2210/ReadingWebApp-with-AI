from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ReadingSession:

    article_name: str = ""

    article_text: str = ""

    words: List[str] = field(default_factory=list)

    current_index: int = 0

    total_words: int = 0

    total_errors: int = 0

    accuracy: float = 0.0

    fluency: float = 0.0

    wpm: float = 0.0

    score: float = 0.0

    completed: bool = False

    attempts: Dict[int, int] = field(default_factory=dict)

    wrong_words: List[str] = field(default_factory=list)

    missing_words: List[str] = field(default_factory=list)

    spoken_words: List[str] = field(default_factory=list)

    # ======================================================
    # LOAD ARTICLE
    # ======================================================

    def load(self, article_name: str, article_text: str):

        self.article_name = article_name

        self.article_text = article_text.strip()

        self.words = self.article_text.split()

        self.total_words = len(self.words)

        self.current_index = 0

        self.total_errors = 0

        self.accuracy = 0

        self.fluency = 0

        self.wpm = 0

        self.score = 0

        self.completed = False

        self.attempts.clear()

        self.wrong_words.clear()

        self.missing_words.clear()

        self.spoken_words.clear()

    # ======================================================
    # CURRENT WORD
    # ======================================================

    def current_word(self):

        if self.current_index >= self.total_words:

            return None

        return self.words[self.current_index]

    # ======================================================
    # NEXT WORD
    # ======================================================

    def next_word(self):

        self.current_index += 1

        if self.current_index >= self.total_words:

            self.completed = True

    # ======================================================
    # ADD SPOKEN WORD
    # ======================================================

    def add_spoken_word(self, word):

        self.spoken_words.append(word)

    # ======================================================
    # ADD ERROR
    # ======================================================

    def add_error(self, word):

        self.total_errors += 1

        self.wrong_words.append(word)

    # ======================================================
    # ADD MISSING
    # ======================================================

    def add_missing(self, word):

        self.missing_words.append(word)

    # ======================================================
    # ADD ATTEMPT
    # ======================================================

    def increase_attempt(self):

        idx = self.current_index

        self.attempts[idx] = self.attempts.get(idx, 0) + 1

    # ======================================================
    # GET ATTEMPT
    # ======================================================

    def current_attempt(self):

        return self.attempts.get(self.current_index, 0)

    # ======================================================
    # RESET
    # ======================================================

    def reset(self):

        self.load("", "")

    # ======================================================
    # SESSION INFO
    # ======================================================

    def summary(self):

        return {

            "Article": self.article_name,

            "Words": self.total_words,

            "Completed": self.completed,

            "Accuracy": self.accuracy,

            "Fluency": self.fluency,

            "Score": self.score,

            "Errors": self.total_errors,

            "Current Word": self.current_word(),

            "Attempts": self.current_attempt(),

        }