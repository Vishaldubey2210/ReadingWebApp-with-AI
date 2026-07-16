"""
==========================================================
ReadingAI

Article Service

==========================================================
"""

import json
import random
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

from config import ARTICLES_DIR
from core.models.article import Article


class ArticleService:

    def __init__(self):
        self.articles: List[Article] = []
        self.validation_logs: List[str] = []
        self.scan_articles()

    def scan_articles(self):
        self.articles = []
        self.validation_logs = []
        
        articles_path = Path(ARTICLES_DIR)
        if not articles_path.exists():
            self.validation_logs.append(f"Articles directory does not exist: {ARTICLES_DIR}")
            return

        # Walk through ARTICLES_DIR
        # Expected structure: articles/{source}/{language}/{difficulty}/{category}/{filename}.txt
        for txt_file in articles_path.glob("**/*.txt"):
            try:
                rel_parts = txt_file.relative_to(articles_path).parts
                if len(rel_parts) < 5:
                    self.validation_logs.append(
                        f"Skipping file with invalid path structure: {txt_file.relative_to(articles_path)}"
                    )
                    continue
                
                source = rel_parts[0]
                lang_code = rel_parts[1]
                diff_code = rel_parts[2]
                category = rel_parts[3]
                article_id = txt_file.stem
                
                # Check for empty content
                content = txt_file.read_text(encoding="utf-8").strip()
                if not content:
                    self.validation_logs.append(f"Empty article content in: {txt_file.relative_to(articles_path)}")
                    continue
                
                # Normalize language code to display name
                language = "English" if lang_code.lower() == "en" else lang_code.capitalize()
                
                # Normalize difficulty code to standard capitalization
                difficulty = diff_code.capitalize() # e.g. easy -> Easy, medium -> Medium, hard -> Hard
                
                # Load metadata JSON if exists
                json_file = txt_file.with_suffix(".json")
                title = article_id.replace("_", " ").title()
                author = "Unknown"
                tags = []
                
                if json_file.exists():
                    try:
                        meta = json.loads(json_file.read_text(encoding="utf-8"))
                        title = meta.get("title", title)
                        author = meta.get("author", author)
                        tags = meta.get("tags", tags)
                    except Exception as je:
                        self.validation_logs.append(
                            f"Failed to parse metadata JSON for {txt_file.relative_to(articles_path)}: {je}"
                        )
                else:
                    self.validation_logs.append(
                        f"Missing metadata JSON file for: {txt_file.relative_to(articles_path)}"
                    )

                article = Article(
                    id=article_id,
                    title=title,
                    content=content,
                    difficulty=difficulty,
                    category=category,
                    language=language,
                    source=source,
                    author=author,
                    tags=tags
                )
                self.articles.append(article)
            except Exception as e:
                self.validation_logs.append(f"Error scanning article {txt_file}: {e}")

    def get_difficulties(self) -> List[str]:
        diffs = list(set(a.difficulty for a in self.articles))
        order = {"Easy": 0, "Medium": 1, "Hard": 2}
        return sorted(diffs, key=lambda d: order.get(d, 99))

    def get_languages(self) -> List[str]:
        return sorted(list(set(a.language for a in self.articles)))

    def get_categories(self, language: str, difficulty: str) -> List[str]:
        categories = set()
        for a in self.articles:
            if a.language.lower() == language.lower() and a.difficulty.lower() == difficulty.lower():
                categories.add(a.category)
        return sorted(list(categories))

    def get_random_article(self, difficulty: str, language: str, category: str) -> Optional[Article]:
        matching = [
            a for a in self.articles
            if a.difficulty.lower() == difficulty.lower()
            and a.language.lower() == language.lower()
            and a.category.lower() == category.lower()
        ]
        if not matching:
            return None
        return random.choice(matching)

    def get_validation_logs(self) -> List[str]:
        return self.validation_logs


_article_service_instance = None


def get_article_service() -> ArticleService:
    global _article_service_instance
    if _article_service_instance is None:
        _article_service_instance = ArticleService()
    return _article_service_instance