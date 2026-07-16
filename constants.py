"""
==========================================================
ReadingAI Constants
==========================================================
"""

SUPPORTED_LANGUAGES = [
    "English"
]

DIFFICULTY_LEVELS = [
    "Easy",
    "Medium",
    "Hard"
]

WHISPER_MODELS = [
    "tiny",
    "base",
    "small",
    "medium",
    "large"
]

STATUS_PENDING = "Pending"
STATUS_READING = "Reading"
STATUS_COMPLETED = "Completed"

GREEN = "#16a34a"
RED = "#dc2626"
BLUE = "#2563eb"
YELLOW = "#f59e0b"
GRAY = "#6b7280"

SUCCESS_ICON = "✅"
ERROR_ICON = "❌"
WARNING_ICON = "⚠️"
MIC_ICON = "🎤"
BOOK_ICON = "📖"
REPORT_ICON = "📊"

FIRST_HINT = 3
SECOND_HINT = 6
FINAL_HINT = 10

MIN_SIMILARITY = 85
MAX_WORD_ATTEMPTS = 10

MIN_WPM = 80
MAX_WPM = 180

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION = 2

DATABASE_NAME = "student.db"

REPORT_FORMAT = "pdf"

DEFAULT_ARTICLE = "easy"