"""
==========================================================
ReadingAI Pronunciation Engine
==========================================================
"""

from rapidfuzz import fuzz
import re


class PronunciationEngine:

    def __init__(self):
        self.accept_threshold = 90
        self.good_threshold = 80
        self.average_threshold = 65

    def clean(self, word):
        word = word.lower()
        word = re.sub(r"[^a-z']", "", word)
        return word.strip()

    def score(self, expected, spoken):
        expected = self.clean(expected)
        spoken = self.clean(spoken)
        if expected == "" or spoken == "":
            return 0
        return fuzz.ratio(expected, spoken)

    def accepted(self, expected, spoken):
        return self.score(expected, spoken) >= self.accept_threshold

    def level(self, score):
        if score >= 95:
            return "Excellent"
        if score >= self.good_threshold:
            return "Good"
        if score >= self.average_threshold:
            return "Average"
        return "Poor"

    def stars(self, score):
        if score >= 95:
            return 5
        if score >= 85:
            return 4
        if score >= 70:
            return 3
        if score >= 50:
            return 2
        return 1

    def color(self, score):
        if score >= 90:
            return "#16a34a"
        if score >= 70:
            return "#f59e0b"
        return "#dc2626"

    def feedback(self, expected, spoken):
        score = self.score(expected, spoken)
        return {
            "expected": expected,
            "spoken": spoken,
            "score": score,
            "level": self.level(score),
            "stars": self.stars(score),
            "accepted": self.accepted(expected, spoken),
            "color": self.color(score)
        }

    def confidence(self, expected, spoken):
        score = self.score(expected, spoken)
        if score >= 95:
            return 1.00
        if score >= 90:
            return 0.95
        if score >= 80:
            return 0.90
        if score >= 70:
            return 0.80
        if score >= 60:
            return 0.70
        return 0.50

    def suggestion(self, score):
        if score >= 95:
            return "Excellent Pronunciation"
        if score >= 85:
            return "Very Good"
        if score >= 70:
            return "Practice Once"
        if score >= 50:
            return "Practice Multiple Times"
        return "Listen Carefully And Repeat"

    def progress(self, score):
        return score / 100

    def html(self, expected, spoken):
        result = self.feedback(expected, spoken)
        return f'<div style="border-radius:12px;padding:20px;border:2px solid {result["color"]};"><h3>{result["expected"]}</h3><p>Spoken : <b>{result["spoken"]}</b></p><p>Score : {result["score"]}%</p><p>Rating : {result["level"]}</p></div>'

    def result(self, expected, spoken):
        score = self.score(expected, spoken)
        return {
            "expected": expected,
            "spoken": spoken,
            "score": score,
            "confidence": self.confidence(expected, spoken),
            "accepted": self.accepted(expected, spoken),
            "stars": self.stars(score),
            "level": self.level(score),
            "suggestion": self.suggestion(score),
            "color": self.color(score)
        }