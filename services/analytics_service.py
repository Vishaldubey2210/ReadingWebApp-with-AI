"""
==========================================================
ReadingAI

Analytics Service

==========================================================
"""

from collections import Counter

from database.database import Database


class AnalyticsService:

    def __init__(self):

        self.db = Database()

    # =====================================================

    def total_sessions(self):

        return self.db.total_sessions()

    # =====================================================

    def average_accuracy(self):

        return self.db.average_accuracy()

    # =====================================================

    def average_score(self):

        return self.db.average_score()

    # =====================================================

    def history(self):

        return self.db.all_results()

    # =====================================================

    def latest(self):

        return self.db.latest()
        # =====================================================

    def best_score(self):

        history = self.history()

        if len(history) == 0:

            return 0

        return max(

            row[7]

            for row in history

        )

    # =====================================================

    def best_accuracy(self):

        history = self.history()

        if len(history) == 0:

            return 0

        return max(

            row[3]

            for row in history

        )

    # =====================================================

    def average_wpm(self):

        history = self.history()

        if len(history) == 0:

            return 0

        return round(

            sum(

                row[6]

                for row in history

            )

            /

            len(history),

            2

        )
        # =====================================================

    def trend(self):

        history = self.history()

        scores = [

            row[7]

            for row in history

        ]

        return scores

    # =====================================================

    def improvement(self):

        history = self.history()

        if len(history) < 2:

            return 0

        return round(

            history[0][7]

            -

            history[-1][7],

            2

        )

    # =====================================================

    def recommendation(self):

        accuracy = self.average_accuracy()

        if accuracy >= 90:

            return "Hard"

        if accuracy >= 70:

            return "Medium"

        return "Easy"
        # =====================================================

    def dashboard(self):

        return {

            "sessions":

            self.total_sessions(),

            "accuracy":

            self.average_accuracy(),

            "score":

            self.average_score(),

            "best_accuracy":

            self.best_accuracy(),

            "best_score":

            self.best_score(),

            "average_wpm":

            self.average_wpm(),

            "difficulty":

            self.recommendation()

        }
    