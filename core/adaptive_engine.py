"""
==========================================================
ReadingAI

Adaptive Learning Engine

==========================================================
"""

from collections import Counter


class AdaptiveEngine:

    def __init__(self):

        self.minimum_accuracy = 75

        self.minimum_pronunciation = 70

        self.minimum_similarity = 80

    # =====================================================

    def difficulty(

        self,

        accuracy

    ):

        if accuracy >= 95:

            return "Hard"

        if accuracy >= 80:

            return "Medium"

        return "Easy"

    # =====================================================

    def reading_level(

        self,

        wpm

    ):

        if wpm >= 150:

            return "Advanced"

        if wpm >= 100:

            return "Intermediate"

        return "Beginner"

    # =====================================================

    def recommendation(

        self,

        accuracy,

        wpm

    ):

        return {

            "difficulty":

            self.difficulty(

                accuracy

            ),

            "reading_level":

            self.reading_level(

                wpm

            )

        }
        # =====================================================

    def weak_words(

        self,

        history

    ):

        words = []

        for row in history:

            expected = row[2]

            similarity = row[4]

            if similarity < self.minimum_similarity:

                words.append(

                    expected

                )

        return Counter(

            words

        ).most_common(20)

    # =====================================================

    def strong_words(

        self,

        history

    ):

        words = []

        for row in history:

            expected = row[2]

            similarity = row[4]

            if similarity >= 95:

                words.append(

                    expected

                )

        return Counter(

            words

        ).most_common(20)
        # =====================================================

    def difficult_sounds(

        self,

        history

    ):

        sounds = Counter()

        for row in history:

            word = row[2].lower()

            similarity = row[4]

            if similarity >= 80:

                continue

            if "th" in word:

                sounds["TH"] += 1

            if "ph" in word:

                sounds["PH"] += 1

            if "sh" in word:

                sounds["SH"] += 1

            if "ch" in word:

                sounds["CH"] += 1

            if "tion" in word:

                sounds["TION"] += 1

            if "ough" in word:

                sounds["OUGH"] += 1

        return sounds.most_common()
        # =====================================================

    def next_article_level(

        self,

        accuracy,

        pronunciation,

        wpm

    ):

        if (

            accuracy >= 90

            and

            pronunciation >= 90

            and

            wpm >= 130

        ):

            return "Hard"

        if (

            accuracy >= 75

            and

            pronunciation >= 70

        ):

            return "Medium"

        return "Easy"
        # =====================================================

    def summary(

        self,

        history,

        accuracy,

        pronunciation,

        wpm

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

            self.difficult_sounds(

                history

            ),

            "next_level":

            self.next_article_level(

                accuracy,

                pronunciation,

                wpm

            )

        }
    