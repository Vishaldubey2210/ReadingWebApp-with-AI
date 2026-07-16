"""
==========================================================
ReadingAI Database
SQLite Database Manager
==========================================================
"""

import sqlite3
from pathlib import Path

from config import DATABASE_DIR


DATABASE_PATH = DATABASE_DIR / "student.db"


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(

            DATABASE_PATH,

            check_same_thread=False

        )

        self.cursor = self.connection.cursor()

        self.create_tables()

    # =====================================================

    def create_tables(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS reading_history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            student_name TEXT,

            article_name TEXT,

            accuracy REAL,

            fluency REAL,

            pronunciation REAL,

            wpm REAL,

            score REAL,

            total_words INTEGER,

            correct_words INTEGER,

            wrong_words INTEGER,

            attempts INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        self.connection.commit()

    # =====================================================

    def insert_result(

        self,

        student_name,

        article_name,

        accuracy,

        fluency,

        pronunciation,

        wpm,

        score,

        total_words,

        correct_words,

        wrong_words,

        attempts

    ):

        self.cursor.execute(

        """

        INSERT INTO reading_history(

        student_name,

        article_name,

        accuracy,

        fluency,

        pronunciation,

        wpm,

        score,

        total_words,

        correct_words,

        wrong_words,

        attempts

        )

        VALUES(

        ?,?,?,?,?,?,?,?,?,?,?,?

        )

        """,

        (

        student_name,

        article_name,

        accuracy,

        fluency,

        pronunciation,

        wpm,

        score,

        total_words,

        correct_words,

        wrong_words,

        attempts

        )

        )

        self.connection.commit()

    # =====================================================

    def all_results(self):

        self.cursor.execute("""

        SELECT *

        FROM reading_history

        ORDER BY id DESC

        """)

        return self.cursor.fetchall()

    # =====================================================

    def latest(self):

        self.cursor.execute("""

        SELECT *

        FROM reading_history

        ORDER BY id DESC

        LIMIT 1

        """)

        return self.cursor.fetchone()

    # =====================================================

    def delete_all(self):

        self.cursor.execute("""

        DELETE FROM reading_history

        """)

        self.connection.commit()

    # =====================================================

    def total_sessions(self):

        self.cursor.execute("""

        SELECT COUNT(*)

        FROM reading_history

        """)

        return self.cursor.fetchone()[0]

    # =====================================================

    def average_accuracy(self):

        self.cursor.execute("""

        SELECT AVG(accuracy)

        FROM reading_history

        """)

        result = self.cursor.fetchone()[0]

        if result is None:

            return 0

        return round(result,2)

    # =====================================================

    def average_score(self):

        self.cursor.execute("""

        SELECT AVG(score)

        FROM reading_history

        """)

        result = self.cursor.fetchone()[0]

        if result is None:

            return 0

        return round(result,2)

    # =====================================================

    def close(self):

        self.connection.close()
            # =====================================================
    # CREATE TABLES
    # =====================================================

    def create_tables(self):

        self.create_students_table()

        self.create_articles_table()

        self.create_sessions_table()

        self.create_word_history_table()

        self.create_pronunciation_table()

        self.create_weak_words_table()

        self.create_daily_progress_table()

        self.connection.commit()
            # =====================================================
    # STUDENTS
    # =====================================================

    def create_students_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS students(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            age INTEGER,

            class_name TEXT,

            school TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)
            # =====================================================
    # ARTICLES
    # =====================================================

    def create_articles_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS articles(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            article_name TEXT,

            difficulty TEXT,

            total_words INTEGER,

            total_sentences INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)
            # =====================================================
    # READING SESSION
    # =====================================================

    def create_sessions_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS reading_sessions(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            student_id INTEGER,

            article_id INTEGER,

            accuracy REAL,

            fluency REAL,

            pronunciation REAL,

            wpm REAL,

            total_score REAL,

            total_words INTEGER,

            correct_words INTEGER,

            wrong_words INTEGER,

            duration REAL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)
            # =====================================================
    # WORD HISTORY
    # =====================================================

    def create_word_history_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS word_history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            session_id INTEGER,

            expected_word TEXT,

            spoken_word TEXT,

            similarity REAL,

            pronunciation REAL,

            attempts INTEGER,

            hint_used INTEGER,

            time_taken REAL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)
            # =====================================================
    # PRONUNCIATION HISTORY
    # =====================================================

    def create_pronunciation_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS pronunciation_history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            session_id INTEGER,

            word TEXT,

            confidence REAL,

            phoneme_score REAL,

            pronunciation_score REAL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)
            # =====================================================
    # WEAK WORDS
    # =====================================================

    def create_weak_words_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS weak_words(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            word TEXT UNIQUE,

            mistakes INTEGER DEFAULT 1,

            last_score REAL,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)
            # =====================================================
    # DAILY PROGRESS
    # =====================================================

    def create_daily_progress_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS daily_progress(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            student_id INTEGER,

            reading_date TEXT,

            sessions INTEGER,

            average_score REAL,

            average_accuracy REAL,

            average_wpm REAL

        )

        """)
            # =====================================================
    # ADD STUDENT
    # =====================================================

    def add_student(

        self,

        name,

        age,

        class_name,

        school

    ):

        self.cursor.execute(

        """

        INSERT INTO students(

            name,

            age,

            class_name,

            school

        )

        VALUES(

            ?,?,?,?

        )

        """,

        (

            name,

            age,

            class_name,

            school

        )

        )

        self.connection.commit()

        return self.cursor.lastrowid

    # =====================================================
    # GET STUDENT
    # =====================================================

    def get_student(

        self,

        student_id

    ):

        self.cursor.execute(

        """

        SELECT *

        FROM students

        WHERE id=?

        """,

        (

            student_id,

        )

        )

        return self.cursor.fetchone()

    # =====================================================
    # ALL STUDENTS
    # =====================================================

    def all_students(self):

        self.cursor.execute(

        """

        SELECT *

        FROM students

        ORDER BY name

        """

        )

        return self.cursor.fetchall()
        # =====================================================
    # ADD ARTICLE
    # =====================================================

    def add_article(

        self,

        article_name,

        difficulty,

        total_words,

        total_sentences

    ):

        self.cursor.execute(

        """

        INSERT INTO articles(

            article_name,

            difficulty,

            total_words,

            total_sentences

        )

        VALUES(

            ?,?,?,?

        )

        """,

        (

            article_name,

            difficulty,

            total_words,

            total_sentences

        )

        )

        self.connection.commit()

        return self.cursor.lastrowid

    # =====================================================
    # GET ARTICLE
    # =====================================================

    def get_article(

        self,

        article_id

    ):

        self.cursor.execute(

        """

        SELECT *

        FROM articles

        WHERE id=?

        """,

        (

            article_id,

        )

        )

        return self.cursor.fetchone()
        # =====================================================
    # START SESSION
    # =====================================================

    def start_session(

        self,

        student_id,

        article_id

    ):

        self.cursor.execute(

        """

        INSERT INTO reading_sessions(

            student_id,

            article_id,

            accuracy,

            fluency,

            pronunciation,

            wpm,

            total_score,

            total_words,

            correct_words,

            wrong_words,

            duration

        )

        VALUES(

            ?,?,

            0,0,0,0,0,0,0,0,0

        )

        """,

        (

            student_id,

            article_id

        )

        )

        self.connection.commit()

        return self.cursor.lastrowid
        # =====================================================
    # FINISH SESSION
    # =====================================================

    def finish_session(

        self,

        session_id,

        accuracy,

        fluency,

        pronunciation,

        wpm,

        score,

        total_words,

        correct_words,

        wrong_words,

        duration

    ):

        self.cursor.execute(

        """

        UPDATE reading_sessions

        SET

        accuracy=?,

        fluency=?,

        pronunciation=?,

        wpm=?,

        total_score=?,

        total_words=?,

        correct_words=?,

        wrong_words=?,

        duration=?

        WHERE id=?

        """,

        (

            accuracy,

            fluency,

            pronunciation,

            wpm,

            score,

            total_words,

            correct_words,

            wrong_words,

            duration,

            session_id

        )

        )

        self.connection.commit()
            # =====================================================
    # GET SESSION
    # =====================================================

    def get_session(

        self,

        session_id

    ):

        self.cursor.execute(

        """

        SELECT *

        FROM reading_sessions

        WHERE id=?

        """,

        (

            session_id,

        )

        )

        return self.cursor.fetchone()

    # =====================================================
    # ALL SESSIONS
    # =====================================================

    def all_sessions(self):

        self.cursor.execute(

        """

        SELECT *

        FROM reading_sessions

        ORDER BY id DESC

        """

        )

        return self.cursor.fetchall()
        # =====================================================
    # SAVE WORD HISTORY
    # =====================================================

    def save_word(

        self,

        session_id,

        expected_word,

        spoken_word,

        similarity,

        pronunciation,

        attempts,

        hint_used,

        time_taken

    ):

        self.cursor.execute(

        """

        INSERT INTO word_history(

            session_id,

            expected_word,

            spoken_word,

            similarity,

            pronunciation,

            attempts,

            hint_used,

            time_taken

        )

        VALUES(

            ?,?,?,?,?,?,?,?

        )

        """,

        (

            session_id,

            expected_word,

            spoken_word,

            similarity,

            pronunciation,

            attempts,

            hint_used,

            time_taken

        )

        )

        self.connection.commit()

        return self.cursor.lastrowid
        # =====================================================
    # WORD HISTORY
    # =====================================================

    def word_history(

        self,

        session_id

    ):

        self.cursor.execute(

        """

        SELECT *

        FROM word_history

        WHERE session_id=?

        ORDER BY id

        """,

        (

            session_id,

        )

        )

        return self.cursor.fetchall()
        # =====================================================
    # SAVE PRONUNCIATION
    # =====================================================

    def save_pronunciation(

        self,

        session_id,

        word,

        confidence,

        phoneme_score,

        pronunciation_score

    ):

        self.cursor.execute(

        """

        INSERT INTO pronunciation_history(

            session_id,

            word,

            confidence,

            phoneme_score,

            pronunciation_score

        )

        VALUES(

            ?,?,?,?,?,

        )

        """.replace(",)", ")"),

        (

            session_id,

            word,

            confidence,

            phoneme_score,

            pronunciation_score

        )

        )

        self.connection.commit()
            # =====================================================
    # PRONUNCIATION HISTORY
    # =====================================================

    def pronunciation_history(

        self,

        session_id

    ):

        self.cursor.execute(

        """

        SELECT *

        FROM pronunciation_history

        WHERE session_id=?

        ORDER BY id

        """,

        (

            session_id,

        )

        )

        return self.cursor.fetchall()
        # =====================================================
    # UPDATE WEAK WORD
    # =====================================================

    def update_weak_word(

        self,

        word,

        score

    ):

        self.cursor.execute(

        """

        SELECT id,mistakes

        FROM weak_words

        WHERE word=?

        """,

        (

            word,

        )

        )

        row = self.cursor.fetchone()

        if row is None:

            self.cursor.execute(

            """

            INSERT INTO weak_words(

                word,

                mistakes,

                last_score

            )

            VALUES(

                ?,?,?

            )

            """,

            (

                word,

                1,

                score

            )

            )

        else:

            self.cursor.execute(

            """

            UPDATE weak_words

            SET

            mistakes=?,

            last_score=?,

            updated_at=CURRENT_TIMESTAMP

            WHERE word=?

            """,

            (

                row[1] + 1,

                score,

                word

            )

            )

        self.connection.commit()
            # =====================================================
    # TOP WEAK WORDS
    # =====================================================

    def weak_words(

        self,

        limit=20

    ):

        self.cursor.execute(

        """

        SELECT *

        FROM weak_words

        ORDER BY mistakes DESC

        LIMIT ?

        """,

        (

            limit,

        )

        )

        return self.cursor.fetchall()
        # =====================================================
    # DAILY PROGRESS
    # =====================================================

    def save_daily_progress(

        self,

        student_id,

        reading_date,

        sessions,

        accuracy,

        wpm,

        score

    ):

        self.cursor.execute(

        """

        INSERT INTO daily_progress(

            student_id,

            reading_date,

            sessions,

            average_score,

            average_accuracy,

            average_wpm

        )

        VALUES(

            ?,?,?,?,?,?

        )

        """,

        (

            student_id,

            reading_date,

            sessions,

            score,

            accuracy,

            wpm

        )

        )

        self.connection.commit()
            # =====================================================
    # STUDENT DASHBOARD
    # =====================================================

    def student_dashboard(

        self,

        student_id

    ):

        self.cursor.execute(

        """

        SELECT

        COUNT(*),

        AVG(accuracy),

        AVG(total_score),

        AVG(wpm)

        FROM reading_sessions

        WHERE student_id=?

        """,

        (

            student_id,

        )

        )

        return self.cursor.fetchone()
    