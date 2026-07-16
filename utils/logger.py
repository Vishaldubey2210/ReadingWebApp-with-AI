import logging

from pathlib import Path

from config import ROOT_DIR


LOG_FOLDER = ROOT_DIR / "logs"

LOG_FOLDER.mkdir(

    exist_ok=True

)

LOG_FILE = LOG_FOLDER / "reading_ai.log"


logging.basicConfig(

    filename=LOG_FILE,

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)


logger = logging.getLogger("ReadingAI")


def info(message):

    logger.info(message)


def warning(message):

    logger.warning(message)


def error(message):

    logger.error(message)


def critical(message):

    logger.critical(message)