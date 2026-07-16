import random
from pathlib import Path


class ArticleManager:

    def __init__(self, article_directory):

        self.article_directory = Path(article_directory)

    # ======================================================
    # GET LEVEL DIRECTORY
    # ======================================================

    def get_level_directory(self, level: str):

        return self.article_directory / level.lower()

    # ======================================================
    # GET ALL ARTICLES
    # ======================================================

    def get_articles(self, level: str):

        folder = self.get_level_directory(level)

        if not folder.exists():

            return []

        return list(folder.glob("*.txt"))

    # ======================================================
    # RANDOM ARTICLE
    # ======================================================

    def random_article(self, level: str):

        articles = self.get_articles(level)

        if len(articles) == 0:

            return None

        return random.choice(articles)

    # ======================================================
    # LOAD ARTICLE
    # ======================================================

    def load_article(self, article_path):

        article_path = Path(article_path)

        if not article_path.exists():

            return ""

        return article_path.read_text(
            encoding="utf-8"
        )

    # ======================================================
    # RANDOM ARTICLE TEXT
    # ======================================================

    def get_random_article(self, level: str):

        article = self.random_article(level)

        if article is None:

            return None, ""

        text = self.load_article(article)

        return article, text

    # ======================================================
    # TOTAL ARTICLES
    # ======================================================

    def total_articles(self, level: str):

        return len(self.get_articles(level))

    # ======================================================
    # WORD COUNT
    # ======================================================

    @staticmethod
    def word_count(text: str):

        return len(text.split())

    # ======================================================
    # SENTENCE COUNT
    # ======================================================

    @staticmethod
    def sentence_count(text: str):

        if text == "":

            return 0

        return len(
            [
                sentence
                for sentence in text.split(".")
                if sentence.strip()
            ]
        )

    # ======================================================
    # ARTICLE INFO
    # ======================================================

    def article_information(self, article_path):

        text = self.load_article(article_path)

        return {

            "title": Path(article_path).stem,

            "words": self.word_count(text),

            "sentences": self.sentence_count(text),

            "text": text

        }