"""
==========================================================
ReadingAI

Phonics Engine

Converts English Words

↓

Phonemes

↓

Syllables

↓

IPA

==========================================================
"""

import pronouncing
from g2p_en import G2p


class PhonicsEngine:

    def __init__(self):

        self.g2p = G2p()

    # =====================================================

    def normalize(

        self,

        word

    ):

        return word.lower().strip()

    # =====================================================

    def phonemes(

        self,

        word

    ):

        word = self.normalize(word)

        return self.g2p(word)

    # =====================================================

    def cmu(

        self,

        word

    ):

        word = self.normalize(word)

        phones = pronouncing.phones_for_word(

            word

        )

        if len(phones) == 0:

            return ""

        return phones[0]
        # =====================================================

    def syllables(

        self,

        word

    ):

        phones = self.cmu(

            word

        )

        if phones == "":

            return 0

        return pronouncing.syllable_count(

            phones

        )

    # =====================================================

    def stresses(

        self,

        word

    ):

        phones = self.cmu(

            word

        )

        if phones == "":

            return ""

        return pronouncing.stresses(

            phones

        )
            # =====================================================

    def pronunciation(

        self,

        word

    ):

        return {

            "word":

            word,

            "phonemes":

            self.phonemes(

                word

            ),

            "cmu":

            self.cmu(

                word

            ),

            "syllables":

            self.syllables(

                word

            ),

            "stress":

            self.stresses(

                word

            )

        }
        # =====================================================

    def compare(

        self,

        expected,

        spoken

    ):

        p1 = self.phonemes(

            expected

        )

        p2 = self.phonemes(

            spoken

        )

        return {

            "expected": p1,

            "spoken": p2

        }
        # =====================================================

    def future_ai(

        self,

        audio,

        expected

    ):

        """
        Future

        Audio

            ↓

        HuBERT

            ↓

        Wav2Vec2

            ↓

        Phoneme Detection

        """

        return {}
    