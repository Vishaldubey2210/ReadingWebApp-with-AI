"""
==========================================================
ReadingAI Configuration File
Author : Vishal Kumar
Project : ReadingAI
==========================================================
"""

from pathlib import Path
import os

# ==========================================================
# ROOT DIRECTORY
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent

# ==========================================================
# PROJECT FOLDERS
# ==========================================================

ASSETS_DIR = ROOT_DIR / "assets"

ARTICLES_DIR = ROOT_DIR / "articles"

SYSTEM_ARTICLES_DIR = ARTICLES_DIR / "system"

USER_ARTICLES_DIR = ARTICLES_DIR / "user"

AI_ARTICLES_DIR = ARTICLES_DIR / "ai"

AUDIO_DIR = ROOT_DIR / "audio"

TEMP_AUDIO_DIR = AUDIO_DIR / "temp"

RECORDING_DIR = AUDIO_DIR / "recordings"

MODELS_DIR = ROOT_DIR / "models"

WHISPER_MODEL_DIR = MODELS_DIR / "whisper"

CACHE_DIR = MODELS_DIR / "cache"

DATABASE_DIR = ROOT_DIR / "database"

OUTPUT_DIR = ROOT_DIR / "outputs"

REPORT_DIR = OUTPUT_DIR / "reports"

CHART_DIR = OUTPUT_DIR / "charts"

UPLOAD_DIR = ROOT_DIR / "uploads"

# ==========================================================
# UI
# ==========================================================

APP_NAME = "ReadingAI"

APP_VERSION = "1.0.0"

PAGE_TITLE = "ReadingAI"

PAGE_ICON = "📖"

LAYOUT = "wide"

# ==========================================================
# ARTICLE
# ==========================================================

DEFAULT_LANGUAGE = "English"

ARTICLE_LEVELS = [
    "Easy",
    "Medium",
    "Hard"
]

# ==========================================================
# SPEECH
# ==========================================================

WHISPER_MODEL = "base"

LANGUAGE = "en"

SAMPLE_RATE = 16000

# ==========================================================
# SCORING
# ==========================================================

SIMILARITY_THRESHOLD = 85

MAX_ATTEMPTS = 10

# ==========================================================
# COLORS
# ==========================================================

SUCCESS = "#16a34a"

ERROR = "#dc2626"

WARNING = "#f59e0b"

PRIMARY = "#2563eb"

# ==========================================================
# CREATE REQUIRED FOLDERS
# ==========================================================

folders = [

    ASSETS_DIR,

    ARTICLES_DIR,

    SYSTEM_ARTICLES_DIR,

    USER_ARTICLES_DIR,

    AI_ARTICLES_DIR,

    AUDIO_DIR,

    TEMP_AUDIO_DIR,

    RECORDING_DIR,

    MODELS_DIR,

    WHISPER_MODEL_DIR,

    CACHE_DIR,

    DATABASE_DIR,

    OUTPUT_DIR,

    REPORT_DIR,

    CHART_DIR,

    UPLOAD_DIR,

]

for folder in folders:

    folder.mkdir(parents=True, exist_ok=True)

# ==========================================================
# ENVIRONMENT
# ==========================================================

os.environ["TOKENIZERS_PARALLELISM"] = "false"