from rapidfuzz import fuzz
import re


class WordAlignment:

    def __init__(self, threshold=85):

        self.threshold = threshold

    # ======================================================
    # CLEAN WORD
    # ======================================================

    @staticmethod
    def clean(word: str):

        word = word.lower()

        word = re.sub(r"[^a-z']", "", word)

        return word.strip()

    # ======================================================
    # SIMILARITY
    # ======================================================

    def similarity(self, original, spoken):

        original = self.clean(original)

        spoken = self.clean(spoken)

        if original == "" or spoken == "":

            return 0

        return fuzz.ratio(original, spoken)

    # ======================================================
    # WORD MATCH
    # ======================================================

    def is_correct(self, original, spoken):

        score = self.similarity(original, spoken)

        return score >= self.threshold

    # ======================================================
    # WORD RESULT
    # ======================================================

    def compare(self, original, spoken):

        score = self.similarity(original, spoken)

        return {

            "original": original,

            "spoken": spoken,

            "similarity": score,

            "correct": score >= self.threshold

        }

    # ======================================================
    # SENTENCE MATCH
    # ======================================================

    def sentence_compare(self, original_words, spoken_words):

        result = []

        maximum = max(
            len(original_words),
            len(spoken_words)
        )

        for i in range(maximum):

            if i >= len(original_words):

                result.append({

                    "type": "extra",

                    "original": "",

                    "spoken": spoken_words[i],

                    "score": 0

                })

                continue

            if i >= len(spoken_words):

                result.append({

                    "type": "missing",

                    "original": original_words[i],

                    "spoken": "",

                    "score": 0

                })

                continue

            score = self.similarity(

                original_words[i],

                spoken_words[i]

            )

            if score >= self.threshold:

                status = "correct"

            else:

                status = "wrong"

            result.append({

                "type": status,

                "original": original_words[i],

                "spoken": spoken_words[i],

                "score": score

            })

        return result

    # ======================================================
    # NEXT WORD CHECK
    # ======================================================

    def can_move_next(

        self,

        original_word,

        spoken_word

    ):

        return self.is_correct(

            original_word,

            spoken_word

        )

    # ======================================================
    # ERROR TYPE
    # ======================================================

    def error_type(

        self,

        original,

        spoken

    ):

        if spoken == "":

            return "missing"

        if self.is_correct(original, spoken):

            return "correct"

        return "wrong"