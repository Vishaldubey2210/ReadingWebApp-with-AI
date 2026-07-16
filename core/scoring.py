import time
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class WordAlignmentResult:
    index: int
    expected: str
    spoken: str
    status: str  # "correct", "substituted", "skipped", "inserted"
    similarity: float


@dataclass
class ReadingResult:
    accuracy: float
    wpm: float
    reading_time_sec: float
    total_words: int
    correct_words: int
    skipped_words: int
    substituted_words: int
    inserted_words: int
    article_title: str
    article_id: str
    alignments: List[WordAlignmentResult]
    inserted_word_list: List[str]
    transcript: str
    audio_path: str

    def to_dict(self) -> dict:
        return {
            "accuracy": self.accuracy,
            "wpm": self.wpm,
            "reading_time_sec": self.reading_time_sec,
            "total_words": self.total_words,
            "correct_words": self.correct_words,
            "skipped_words": self.skipped_words,
            "substituted_words": self.substituted_words,
            "inserted_words": self.inserted_words,
            "article_title": self.article_title,
            "article_id": self.article_id,
            "alignments": [
                {
                    "index": a.index,
                    "expected": a.expected,
                    "spoken": a.spoken,
                    "status": a.status,
                    "similarity": a.similarity
                }
                for a in self.alignments
            ],
            "inserted_word_list": self.inserted_word_list,
            "transcript": self.transcript,
            "audio_path": self.audio_path
        }


class ReadingScore:

    def __init__(self):

        self.start_time = None

        self.end_time = None

        self.total_words = 0

        self.correct_words = 0

        self.wrong_words = 0

        self.missing_words = 0

    # =====================================================

    def start(self):

        self.start_time = time.time()

    # =====================================================

    def stop(self):

        self.end_time = time.time()

    # =====================================================

    def add_correct(self):

        self.correct_words += 1

        self.total_words += 1

    # =====================================================

    def add_wrong(self):

        self.wrong_words += 1

        self.total_words += 1

    # =====================================================

    def add_missing(self):

        self.missing_words += 1

        self.total_words += 1

    # =====================================================

    def duration(self):

        if self.start_time is None:

            return 0

        end = self.end_time if self.end_time else time.time()

        return end - self.start_time

    # =====================================================

    def accuracy(self):

        if self.total_words == 0:

            return 0

        return round(

            (self.correct_words / self.total_words) * 100,

            2

        )

    # =====================================================

    def error_rate(self):

        if self.total_words == 0:

            return 0

        errors = self.wrong_words + self.missing_words

        return round(

            (errors / self.total_words) * 100,

            2

        )

    # =====================================================

    def words_per_minute(self):

        seconds = self.duration()

        if seconds == 0:

            return 0

        minutes = seconds / 60

        return round(

            self.correct_words / minutes,

            2

        )

    # =====================================================

    def fluency(self):

        accuracy = self.accuracy()

        wpm = self.words_per_minute()

        score = (accuracy * 0.7)

        score += min(wpm, 150) * 0.2

        score += 10

        return min(round(score, 2), 100)

    # =====================================================

    def final_score(self):

        accuracy = self.accuracy()

        fluency = self.fluency()

        return round(

            (accuracy * 0.6) +

            (fluency * 0.4),

            2

        )

    # =====================================================

    def summary(self):

        return {

            "total_words": self.total_words,

            "correct_words": self.correct_words,

            "wrong_words": self.wrong_words,

            "missing_words": self.missing_words,

            "accuracy": self.accuracy(),

            "error_rate": self.error_rate(),

            "wpm": self.words_per_minute(),

            "fluency": self.fluency(),

            "score": self.final_score(),

            "duration": round(self.duration(), 2)

        }

    # =====================================================

    def reset(self):

        self.__init__()