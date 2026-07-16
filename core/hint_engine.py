from dataclasses import dataclass


@dataclass
class Hint:

    english: str

    pronunciation: str

    meaning: str


class HintEngine:

    def __init__(self):

        self.dictionary = {

            "elephant": Hint(
                "Elephant",
                "ए-लि-फन्ट",
                "हाथी"
            ),

            "beautiful": Hint(
                "Beautiful",
                "ब्यू-टी-फुल",
                "सुन्दर"
            ),

            "through": Hint(
                "Through",
                "थ्रू",
                "के माध्यम से"
            ),

            "psychology": Hint(
                "Psychology",
                "साइ-को-लॉ-जी",
                "मनोविज्ञान"
            ),

            "architecture": Hint(
                "Architecture",
                "आर-कि-टेक्चर",
                "वास्तुकला"
            ),

            "environment": Hint(
                "Environment",
                "इन-वाइ-रन-मेंट",
                "पर्यावरण"
            ),

            "knowledge": Hint(
                "Knowledge",
                "नॉ-लेज",
                "ज्ञान"
            ),

            "language": Hint(
                "Language",
                "लैंग-ग्विज",
                "भाषा"
            ),

            "technology": Hint(
                "Technology",
                "टेक-नॉ-ल-जी",
                "तकनीक"
            ),

            "computer": Hint(
                "Computer",
                "कम-प्यू-टर",
                "कंप्यूटर"
            )

        }

    # =====================================================

    def normalize(self, word):

        return word.lower().strip()

    # =====================================================

    def available(self, word):

        return self.normalize(word) in self.dictionary

    # =====================================================

    def pronunciation(self, word):

        word = self.normalize(word)

        if word not in self.dictionary:

            return ""

        return self.dictionary[word].pronunciation

    # =====================================================

    def meaning(self, word):

        word = self.normalize(word)

        if word not in self.dictionary:

            return ""

        return self.dictionary[word].meaning

    # =====================================================

    def hint(self, word):

        word = self.normalize(word)

        if word not in self.dictionary:

            return {

                "word": word,

                "pronunciation": "",

                "meaning": ""

            }

        data = self.dictionary[word]

        return {

            "word": data.english,

            "pronunciation": data.pronunciation,

            "meaning": data.meaning

        }

    # =====================================================

    def should_show_hint(self, attempts):

        return attempts >= 3

    # =====================================================

    def should_show_pronunciation(self, attempts):

        return attempts >= 6

    # =====================================================

    def should_show_meaning(self, attempts):

        return attempts >= 10

    # =====================================================

    def build_hint(self, word, attempts):

        result = {

            "show": False,

            "pronunciation": "",

            "meaning": ""

        }

        if not self.should_show_hint(attempts):

            return result

        result["show"] = True

        if self.should_show_pronunciation(attempts):

            result["pronunciation"] = self.pronunciation(word)

        if self.should_show_meaning(attempts):

            result["meaning"] = self.meaning(word)

        return result