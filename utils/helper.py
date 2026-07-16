from datetime import datetime


def current_time():

    return datetime.now()


def current_time_string():

    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def words(text: str):

    return text.split()


def total_words(text: str):

    return len(words(text))


def clean_spaces(text: str):

    return " ".join(text.split())


def percentage(value, total):

    if total == 0:

        return 0

    return round((value / total) * 100, 2)