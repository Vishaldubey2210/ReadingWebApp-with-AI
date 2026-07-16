from pathlib import Path


class FileUtils:

    @staticmethod
    def read(path):

        return Path(path).read_text(

            encoding="utf-8"

        )

    @staticmethod
    def write(path, text):

        Path(path).write_text(

            text,

            encoding="utf-8"

        )

    @staticmethod
    def exists(path):

        return Path(path).exists()

    @staticmethod
    def filename(path):

        return Path(path).stem

    @staticmethod
    def extension(path):

        return Path(path).suffix

    @staticmethod
    def list_files(folder):

        folder = Path(folder)

        if not folder.exists():

            return []

        return list(folder.glob("*"))

    @staticmethod
    def list_articles(folder):

        folder = Path(folder)

        if not folder.exists():

            return []

        return list(folder.glob("*.txt"))