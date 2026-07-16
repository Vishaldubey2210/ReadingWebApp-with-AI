"""
==========================================================
ReadingAI

Pronunciation Service

==========================================================
"""

from core.pronunciation import PronunciationEngine
from core.phoneme_engine import PhonemeEngine


class PronunciationService:

    def __init__(self):

        self.engine = PronunciationEngine()

        self.phoneme = PhonemeEngine()

    # =====================================================

    def evaluate(

        self,

        expected,

        spoken

    ):

        pronunciation = self.engine.result(

            expected,

            spoken

        )

        pronunciation["phoneme"] = self.phoneme.pronunciation_card(

            expected

        )

        return pronunciation

    # =====================================================

    def score(

        self,

        expected,

        spoken

    ):

        return self.engine.score(

            expected,

            spoken

        )

    # =====================================================

    def accepted(

        self,

        expected,

        spoken

    ):

        return self.engine.accepted(

            expected,

            spoken

        )

    # =====================================================

    def confidence(

        self,

        expected,

        spoken

    ):

        return self.engine.confidence(

            expected,

            spoken

        )

    # =====================================================

    def html(

        self,

        expected,

        spoken

    ):

        return self.engine.html(

            expected,

            spoken

        )

    # =====================================================

    def pronunciation_hint(

        self,

        word,

        attempts

    ):

        return self.phoneme.hint(

            word,

            attempts

        )

    # =====================================================

    def pronunciation_card(

        self,

        word

    ):

        return self.phoneme.pronunciation_card(

            word

        )
        # =====================================================

    def detailed_result(

        self,

        expected,

        spoken,

        attempts

    ):

        return {

            "pronunciation":

            self.evaluate(

                expected,

                spoken

            ),

            "hint":

            self.pronunciation_hint(

                expected,

                attempts

            ),

            "card":

            self.pronunciation_card(

                expected

            )

        }

    # =====================================================

    def future_ai(

        self,

        audio,

        expected

    ):

        return self.phoneme.ai_pronunciation(

            audio,

            expected

        )

    # =====================================================

    def reset(self):

        pass
    