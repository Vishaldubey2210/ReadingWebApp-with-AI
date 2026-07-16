"""
==========================================================
ReadingAI Phoneme Engine
==========================================================
"""

import re


class PhonemeEngine:

    def __init__(self):
        self.dictionary = {
            "beautiful": {
                "syllables": ["Beau", "ti", "ful"],
                "hindi": "ब्यू-टी-फुल"
            },
            "elephant": {
                "syllables": ["El", "e", "phant"],
                "hindi": "ए-लि-फन्ट"
            },
            "computer": {
                "syllables": ["Com", "pu", "ter"],
                "hindi": "कम-प्यू-टर"
            },
            "environment": {
                "syllables": ["En", "vi", "ron", "ment"],
                "hindi": "इन-वाइ-रन-मेंट"
            }
        }

    def clean(self, word):
        word = word.lower()
        word = re.sub(r"[^a-z]", "", word)
        return word

    def exists(self, word):
        return self.clean(word) in self.dictionary

    def syllables(self, word):
        word = self.clean(word)
        if word not in self.dictionary:
            return []
        return self.dictionary[word]["syllables"]

    def hindi(self, word):
        word = self.clean(word)
        if word not in self.dictionary:
            return ""
        return self.dictionary[word]["hindi"]

    def total_syllables(self, word):
        return len(self.syllables(word))

    def syllable_text(self, word):
        return " - ".join(self.syllables(word))

    def pronunciation_card(self, word):
        return {
            "word": word,
            "syllables": self.syllables(word),
            "syllable_text": self.syllable_text(word),
            "hindi": self.hindi(word),
            "count": self.total_syllables(word)
        }

    def hint(self, word, attempts):
        result = {
            "show": False,
            "syllables": [],
            "hindi": ""
        }
        if attempts < 3:
            return result
        result["show"] = True
        if attempts >= 3:
            result["syllables"] = self.syllables(word)
        if attempts >= 6:
            result["hindi"] = self.hindi(word)
        return result

    def html(self, word, attempts):
        hint = self.hint(word, attempts)
        if not hint["show"]:
            return ""
        html = f'<div style="border:2px solid #2563eb;border-radius:12px;padding:20px;margin-top:20px;"><h3>💡 Pronunciation Hint</h3>'
        if len(hint["syllables"]) != 0:
            html += f'<h4>{" - ".join(hint["syllables"])}</h4>'
        if hint["hindi"] != "":
            html += f'<h3>{hint["hindi"]}</h3>'
        html += "</div>"
        return html

    def ai_pronunciation(self, audio, expected_word):
        """
        Future Deep Learning Model

        Input:
            Audio
            Expected Word

        Output:
            Pronunciation Score
        """
        return {
            "score": 0,
            "phoneme_accuracy": 0,
            "stress_accuracy": 0,
            "intonation": 0,
            "accepted": False
        }

    def reset(self):
        pass