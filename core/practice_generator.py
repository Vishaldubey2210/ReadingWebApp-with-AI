"""
==========================================================
ReadingAI

Practice Generator Engine

Generates Personalized Practice Words
Based on Student Weak Pronunciation Patterns

==========================================================
"""

from collections import defaultdict
from typing import List, Dict


class PracticeGenerator:

    def __init__(self):

        self.practice_sets = defaultdict(list)

        self.load_builtin_words()

    # =====================================================
    # LOAD BUILT-IN PRACTICE SETS
    # =====================================================

    def load_builtin_words(self):

        self.practice_sets["TH"] = [
            "think",
            "three",
            "throw",
            "through",
            "thought",
            "throat",
            "thread",
            "thrive",
            "thunder",
            "thousand",
            "there",
            "their",
            "these",
            "those",
            "thick",
            "thin",
            "thank",
            "theme",
            "thermal",
            "therapy"
        ]

        self.practice_sets["SH"] = [
            "ship",
            "shop",
            "share",
            "shine",
            "shadow",
            "shape",
            "shark",
            "shout",
            "should",
            "sharp",
            "sheep",
            "shirt",
            "shell",
            "shower",
            "show",
            "short",
            "shelf",
            "shrimp",
            "shiver",
            "shampoo"
        ]

        self.practice_sets["CH"] = [
            "chair",
            "chalk",
            "change",
            "choice",
            "child",
            "chapter",
            "chicken",
            "cheese",
            "church",
            "challenge",
            "chance",
            "charge",
            "champion",
            "chase",
            "chain",
            "cherry",
            "chess",
            "cheer",
            "chemist",
            "chocolate"
        ]

        self.practice_sets["PH"] = [
            "phone",
            "photo",
            "phrase",
            "physics",
            "pharmacy",
            "phonics",
            "phantom",
            "philosophy",
            "photograph",
            "phenomenon"
        ]

        self.practice_sets["OUGH"] = [
            "through",
            "thought",
            "rough",
            "though",
            "brought",
            "enough",
            "throughout",
            "tough",
            "cough",
            "dough"
        ]

        self.practice_sets["TION"] = [
            "education",
            "information",
            "station",
            "nation",
            "action",
            "communication",
            "production",
            "relation",
            "question",
            "attention"
        ]

        self.practice_sets["EA"] = [
            "eat",
            "each",
            "eagle",
            "teacher",
            "reading",
            "dream",
            "clean",
            "reason",
            "peace",
            "please"
        ]

        self.practice_sets["OO"] = [
            "book",
            "look",
            "good",
            "food",
            "school",
            "room",
            "moon",
            "boot",
            "wood",
            "football"
        ]

    # =====================================================
    # DETECT SOUND PATTERN
    # =====================================================

    def detect_pattern(self, word: str):

        word = word.lower()

        patterns = [

            "ough",
            "tion",
            "th",
            "sh",
            "ch",
            "ph",
            "wh",
            "ck",
            "ea",
            "ee",
            "oo",
            "ai",
            "ay",
            "oi",
            "oy"

        ]

        for pattern in patterns:

            if pattern in word:

                return pattern.upper()

        return None

    # =====================================================
    # PRACTICE FOR SINGLE WORD
    # =====================================================

    def generate(self, word: str):

        pattern = self.detect_pattern(word)

        if pattern is None:

            return [word]

        return self.practice_sets.get(pattern, [word])

    # =====================================================
    # PRACTICE FOR MULTIPLE WORDS
    # =====================================================

    def personalized(self, weak_words: List[str]):

        practice = []

        visited = set()

        for word in weak_words:

            words = self.generate(word)

            for item in words:

                if item not in visited:

                    practice.append(item)

                    visited.add(item)

        return practice

    # =====================================================
    # DAILY PRACTICE
    # =====================================================

    def daily_practice(

        self,

        weak_words,

        limit=20

    ):

        practice = self.personalized(

            weak_words

        )

        return practice[:limit]

    # =====================================================
    # WEEKLY PRACTICE
    # =====================================================

    def weekly_practice(

        self,

        weak_words,

        limit=50

    ):

        practice = self.personalized(

            weak_words

        )

        return practice[:limit]

    # =====================================================
    # RECOMMENDED DIFFICULTY
    # =====================================================

    def recommendation(

        self,

        dashboard

    ):

        accuracy = dashboard.get(

            "accuracy",

            0

        )

        if accuracy >= 95:

            return {

                "difficulty": "Hard",

                "practice_words": 5

            }

        if accuracy >= 80:

            return {

                "difficulty": "Medium",

                "practice_words": 10

            }

        return {

            "difficulty": "Easy",

            "practice_words": 20

        }

    # =====================================================
    # COMPLETE REPORT
    # =====================================================

    def report(

        self,

        weak_words,

        dashboard

    ):

        return {

            "recommended_difficulty":

                self.recommendation(

                    dashboard

                ),

            "practice_words":

                self.daily_practice(

                    weak_words

                ),

            "total_practice_words":

                len(

                    self.daily_practice(

                        weak_words

                    )

                )

        }

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        pass