"""
============================================================
ReadingAI

Live Reading Controller

============================================================
"""

from typing import Optional

from core.word_alignment import WordAlignment

from core.hint_engine import HintEngine

from core.pronunciation import PronunciationEngine

from core.reading_session import ReadingSession

from core.scoring import ReadingScore


class LiveReader:

    """
    Reading Controller

    Controls

    • Current Word

    • Progress

    • Attempts

    • Hint

    • Pronunciation

    • Score

    """

    def __init__(self):

        self.session = ReadingSession()

        self.aligner = WordAlignment()

        self.pronunciation = PronunciationEngine()

        self.hint = HintEngine()

        self.score = ReadingScore()

        self.started = False

        self.finished = False

    # =====================================================

    def load_article(

        self,

        article_name: str,

        article_text: str

    ):

        self.session.load(

            article_name,

            article_text

        )

        self.started = False

        self.finished = False

    # =====================================================

    def start(self):

        if self.started:

            return

        self.started = True

        self.score.start()

    # =====================================================

    def stop(self):

        if self.finished:

            return

        self.score.stop()

        self.finished = True

    # =====================================================

    def current_word(self):

        return self.session.current_word()

    # =====================================================

    def total_words(self):

        return self.session.total_words

    # =====================================================

    def current_index(self):

        return self.session.current_index

    # =====================================================

    def completed(self):

        return self.session.completed
        # =====================================================
    # CURRENT ATTEMPT
    # =====================================================

    def attempts(self):

        return self.session.current_attempt()

    # =====================================================
    # PROCESS SPOKEN WORD
    # =====================================================

    def process(

        self,

        spoken_word: str

    ):

        expected = self.current_word()

        if expected is None:

            self.stop()

            return self.result()

        alignment = self.aligner.compare(

            expected,

            spoken_word

        )

        pronunciation = self.pronunciation.result(

            expected,

            spoken_word

        )

        if alignment["correct"]:

            self.session.add_spoken_word(

                spoken_word

            )

            self.session.next_word()

            self.score.add_correct()

            if self.session.completed:

                self.stop()

        else:

            self.session.add_error(

                spoken_word

            )

            self.session.increase_attempt()

            self.score.add_wrong()

        return {

            "alignment": alignment,

            "pronunciation": pronunciation,

            "hint": self.current_hint(),

            "current_word": self.current_word(),

            "attempts": self.attempts(),

            "completed": self.completed()

        }

    # =====================================================
    # PROCESS TRANSCRIPT
    # =====================================================

    def process_transcript(

        self,

        transcript: str

    ):

        words = transcript.split()

        if len(words) == 0:

            return None

        return self.process(

            words[-1]

        )

    # =====================================================
    # CAN MOVE NEXT
    # =====================================================

    def can_move_next(

        self,

        spoken_word

    ):

        return self.aligner.is_correct(

            self.current_word(),

            spoken_word

        )

    # =====================================================
    # CURRENT PRONUNCIATION
    # =====================================================

    def pronunciation_result(

        self,

        spoken_word

    ):

        return self.pronunciation.result(

            self.current_word(),

            spoken_word

        )
        # =====================================================
    # CURRENT HINT
    # =====================================================

    def current_hint(self):

        return self.hint.build_hint(

            self.current_word(),

            self.attempts()

        )

    # =====================================================
    # READING PROGRESS
    # =====================================================

    def progress(self):

        if self.total_words() == 0:

            return 0

        return round(

            self.current_index()

            /

            self.total_words(),

            2

        )

    # =====================================================
    # REMAINING WORDS
    # =====================================================

    def remaining_words(self):

        return (

            self.total_words()

            -

            self.current_index()

        )

    # =====================================================
    # COMPLETION
    # =====================================================

    def completion_percentage(self):

        return round(

            self.progress() * 100,

            2

        )

    # =====================================================
    # CURRENT STATUS
    # =====================================================

    def status(self):

        return {

            "started": self.started,

            "finished": self.finished,

            "current_word": self.current_word(),

            "current_index": self.current_index(),

            "remaining_words": self.remaining_words(),

            "progress": self.progress(),

            "completion": self.completion_percentage()

        }
        # =====================================================
    # FINAL RESULT
    # =====================================================

    def result(self):

        return {

            "accuracy": self.score.accuracy(),

            "fluency": self.score.fluency(),

            "score": self.score.final_score(),

            "wpm": self.score.words_per_minute(),

            "duration": self.score.duration(),

            "summary": self.score.summary()

        }

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.session.reset()

        self.score.reset()

        self.started = False

        self.finished = False

    # =====================================================
    # IS RUNNING
    # =====================================================

    def running(self):

        return self.started and not self.finished

    # =====================================================
    # READY
    # =====================================================

    def ready(self):

        return self.session.total_words > 0