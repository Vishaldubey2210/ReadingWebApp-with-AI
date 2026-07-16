"""
==========================================================
ReadingAI

Error Analyzer

Analyzes Reading Errors

Future Deep Learning Compatible

==========================================================
"""

from collections import Counter
from typing import List, Dict


class ErrorAnalyzer:

    def __init__(self):

        self.phoneme_patterns = {

            "TH": ["th"],

            "SH": ["sh"],

            "CH": ["ch"],

            "PH": ["ph"],

            "TION": ["tion"],

            "SION": ["sion"],

            "OUGH": ["ough"],

            "OO": ["oo"],

            "EE": ["ee"],

            "EA": ["ea"],

            "AI": ["ai"],

            "AY": ["ay"],

            "OI": ["oi"],

            "OY": ["oy"],

            "CK": ["ck"],

            "WH": ["wh"]

        }

    # =====================================================
    # NORMALIZE
    # =====================================================

    def normalize(self, word: str):

        return word.lower().strip()

    # =====================================================
    # DETECT PATTERN
    # =====================================================

    def detect_patterns(self, word):

        word = self.normalize(word)

        found = []

        for name, patterns in self.phoneme_patterns.items():

            for pattern in patterns:

                if pattern in word:

                    found.append(name)

                    break

        return found

    # =====================================================
    # ERROR TYPE
    # =====================================================

    def error_type(

        self,

        similarity

    ):

        if similarity >= 95:

            return "Perfect"

        if similarity >= 85:

            return "Minor"

        if similarity >= 70:

            return "Medium"

        return "Major"

    # =====================================================
    # ANALYZE WORD
    # =====================================================

    def analyze_word(

        self,

        expected,

        spoken,

        similarity,

        attempts

    ):

        return {

            "expected": expected,

            "spoken": spoken,

            "similarity": similarity,

            "attempts": attempts,

            "error_type": self.error_type(

                similarity

            ),

            "patterns": self.detect_patterns(

                expected

            )

        }

    # =====================================================
    # ANALYZE HISTORY
    # =====================================================

    def analyze_history(

        self,

        word_history

    ):

        report = []

        for row in word_history:

            report.append(

                self.analyze_word(

                    row[2],

                    row[3],

                    row[4],

                    row[6]

                )

            )

        return report

    # =====================================================
    # WEAK SOUNDS
    # =====================================================

    def weak_sounds(

        self,

        word_history

    ):

        sounds = []

        for row in word_history:

            similarity = row[4]

            if similarity >= 80:

                continue

            sounds.extend(

                self.detect_patterns(

                    row[2]

                )

            )

        return Counter(

            sounds

        ).most_common()

    # =====================================================
    # WEAK WORDS
    # =====================================================

    def weak_words(

        self,

        word_history,

        limit=20

    ):

        words = []

        for row in word_history:

            if row[4] < 80:

                words.append(

                    row[2]

                )

        return Counter(

            words

        ).most_common(

            limit

        )

    # =====================================================
    # STRONG WORDS
    # =====================================================

    def strong_words(

        self,

        word_history,

        limit=20

    ):

        words = []

        for row in word_history:

            if row[4] >= 95:

                words.append(

                    row[2]

                )

        return Counter(

            words

        ).most_common(

            limit

        )

    # =====================================================
    # MOST DIFFICULT WORD
    # =====================================================

    def hardest_word(

        self,

        word_history

    ):

        weak = self.weak_words(

            word_history,

            1

        )

        if len(weak) == 0:

            return None

        return weak[0]

    # =====================================================
    # IMPROVEMENT SCORE
    # =====================================================

    def improvement(

        self,

        previous_accuracy,

        current_accuracy

    ):

        return round(

            current_accuracy -

            previous_accuracy,

            2

        )

    # =====================================================
    # REPORT
    # =====================================================

    def report(

        self,

        history

    ):

        return {

            "weak_words":

                self.weak_words(

                    history

                ),

            "strong_words":

                self.strong_words(

                    history

                ),

            "weak_sounds":

                self.weak_sounds(

                    history

                ),

            "hardest_word":

                self.hardest_word(

                    history

                )

        }

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        pass