import re


class TextUtils:

    @staticmethod
    def normalize(text):

        text = text.lower()

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @staticmethod
    def clean_word(word):

        word = word.lower()

        word = re.sub(r"[^a-z']", "", word)

        return word.strip()

    @staticmethod
    def tokenize(text):

        return [

            TextUtils.clean_word(i)

            for i in text.split()

            if TextUtils.clean_word(i) != ""

        ]

    @staticmethod
    def sentence_count(text):

        return len(

            [

                i

                for i in re.split(

                    r"[.!?]",

                    text

                )

                if i.strip()

            ]

        )

    @staticmethod
    def word_count(text):

        return len(

            TextUtils.tokenize(text)

        )

    @staticmethod
    def average_word_length(text):

        words = TextUtils.tokenize(text)

        if len(words) == 0:

            return 0

        return round(

            sum(

                len(i)

                for i in words

            )

            /

            len(words),

            2

        )