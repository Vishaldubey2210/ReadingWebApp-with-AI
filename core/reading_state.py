"""
=========================================================
ReadingAI

Reading State Machine

=========================================================
"""

from enum import Enum


class ReadingState(Enum):

    IDLE = "idle"

    ARTICLE_LOADED = "article_loaded"

    WAITING = "waiting"

    LISTENING = "listening"

    PROCESSING = "processing"

    CORRECT = "correct"

    WRONG = "wrong"

    SHOW_HINT = "show_hint"

    NEXT_WORD = "next_word"

    FINISHED = "finished"
class ReadingStateController:

    def __init__(self):

        self.state = ReadingState.IDLE

    # ===============================================

    def set_state(

        self,

        state

    ):

        self.state = state

    # ===============================================

    def current(self):

        return self.state

    # ===============================================

    def idle(self):

        return self.state == ReadingState.IDLE

    # ===============================================

    def loaded(self):

        return self.state == ReadingState.ARTICLE_LOADED

    # ===============================================

    def waiting(self):

        return self.state == ReadingState.WAITING

    # ===============================================

    def listening(self):

        return self.state == ReadingState.LISTENING

    # ===============================================

    def processing(self):

        return self.state == ReadingState.PROCESSING

    # ===============================================

    def correct(self):

        return self.state == ReadingState.CORRECT

    # ===============================================

    def wrong(self):

        return self.state == ReadingState.WRONG

    # ===============================================

    def finished(self):

        return self.state == ReadingState.FINISHED
        # ===============================================

    def article_loaded(self):

        self.state = ReadingState.ARTICLE_LOADED

    # ===============================================

    def wait(self):

        self.state = ReadingState.WAITING

    # ===============================================

    def start_listening(self):

        self.state = ReadingState.LISTENING

    # ===============================================

    def process(self):

        self.state = ReadingState.PROCESSING

    # ===============================================

    def word_correct(self):

        self.state = ReadingState.CORRECT

    # ===============================================

    def word_wrong(self):

        self.state = ReadingState.WRONG

    # ===============================================

    def show_hint(self):

        self.state = ReadingState.SHOW_HINT

    # ===============================================

    def next_word(self):

        self.state = ReadingState.NEXT_WORD

    # ===============================================

    def finish(self):

        self.state = ReadingState.FINISHED

    # ===============================================

    def reset(self):

        self.state = ReadingState.IDLE