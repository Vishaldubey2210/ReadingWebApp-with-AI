"""
==========================================================
ReadingAI

Reading Service

Main Business Logic

==========================================================
"""

import time
import os
from core.live_reader import LiveReader
from core.reading_state import (
    ReadingState,
    ReadingStateController,
)


class RecordingSession:
    def __init__(self, article_id: str):
        self.article_id = article_id
        self.start_time = time.time()
        self.end_time = None

    @property
    def elapsed_seconds(self) -> float:
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time


class ReadingService:

    def __init__(self):

        self.reader = LiveReader()

        self.state = ReadingStateController()

        self._speech_engine = None

    # ======================================================

    def load_article(

        self,

        article_name,

        article_text

    ):

        self.reader.load_article(

            article_name,

            article_text

        )

        self.state.article_loaded()

    # ======================================================

    def start(self):

        if not self.reader.ready():

            return False

        self.reader.start()

        self.state.start_listening()

        return True

    # ======================================================

    def stop(self):

        self.reader.stop()

        self.state.finish()

    # ======================================================

    def reset(self):

        self.reader.reset()

        self.state.reset()

    # ======================================================

    def current_state(self):

        return self.state.current()
        # ======================================================

    def current_word(self):

        return self.reader.current_word()

    # ======================================================

    def current_index(self):

        return self.reader.current_index()

    # ======================================================

    def total_words(self):

        return self.reader.total_words()

    # ======================================================

    def progress(self):

        return self.reader.progress()

    # ======================================================

    def completion(self):

        return self.reader.completion_percentage()

    # ======================================================

    def attempts(self):

        return self.reader.attempts()

    # ======================================================

    def finished(self):

        return self.reader.completed()
        # ======================================================

    def process(

        self,

        spoken_word

    ):

        self.state.process()

        result = self.reader.process(

            spoken_word

        )

        if result["completed"]:

            self.state.finish()

            return result

        if result["alignment"]["correct"]:

            self.state.word_correct()

        else:

            self.state.word_wrong()

        return result
        # ======================================================

    def transcript(

        self,

        transcript

    ):

        return self.process(

            transcript.split()[-1]

        )

    # ======================================================

    def hint(self):

        return self.reader.current_hint()

    # ======================================================

    def score(self):

        return self.reader.result()

    # ======================================================

    def running(self):

        return self.reader.running()
        # ======================================================

    def dashboard(self):

        return {

            "state": self.current_state(),

            "current_word": self.current_word(),

            "current_index": self.current_index(),

            "total_words": self.total_words(),

            "progress": self.progress(),

            "completion": self.completion(),

            "attempts": self.attempts(),

            "finished": self.finished(),

            "score": self.score()

        }

    # ======================================================

    def create_session(self, article_id: str) -> RecordingSession:
        return RecordingSession(article_id)

    # ======================================================

    def process_recording(
        self,
        session: RecordingSession,
        audio_file_like,
        article_text: str,
        article_id: str,
        article_title: str,
        language: str = None
    ):
        # Stop session timer
        session.end_time = time.time()
        duration_seconds = max(0.1, session.elapsed_seconds)

        # 1. Save recorded audio bytes to a file
        from config import RECORDING_DIR
        import uuid
        os.makedirs(RECORDING_DIR, exist_ok=True)
        audio_filename = f"session_{uuid.uuid4().hex}_{article_id}.wav"
        audio_path = RECORDING_DIR / audio_filename
        
        audio_data = audio_file_like.read()
        audio_path.write_bytes(audio_data)

        # 2. Transcribe the audio file using SpeechEngine
        from core.speech_engine import SpeechEngine
        
        if self._speech_engine is None:
            self._speech_engine = SpeechEngine()
            
        lang_code = "en"
        if language and language.lower() in ["english", "en"]:
            lang_code = "en"
        self._speech_engine.set_language(lang_code)
        
        transcript = self._speech_engine.transcribe_file(str(audio_path))

        # 3. Perform Word Alignment using Needleman-Wunsch algorithm
        from core.word_alignment import WordAlignment
        from core.scoring import ReadingResult, WordAlignmentResult
        from rapidfuzz import fuzz
        
        words_expected = article_text.split()
        words_spoken = transcript.split()
        
        clean_expected = [WordAlignment.clean(w) for w in words_expected]
        clean_spoken = [WordAlignment.clean(w) for w in words_spoken]
        
        M = len(words_expected)
        N = len(words_spoken)
        
        dp = [[0] * (N + 1) for _ in range(M + 1)]
        
        # Penalties for deletion (skip) and insertion
        skip_penalty = -30
        insert_penalty = -30
        
        for i in range(1, M + 1):
            dp[i][0] = i * skip_penalty
        for j in range(1, N + 1):
            dp[0][j] = j * insert_penalty
            
        for i in range(1, M + 1):
            for j in range(1, N + 1):
                w_exp = clean_expected[i-1]
                w_spk = clean_spoken[j-1]
                
                if not w_exp or not w_spk:
                    sim = 0.0
                else:
                    sim = fuzz.ratio(w_exp, w_spk)
                    
                match_score = dp[i-1][j-1] + sim
                skip_score = dp[i-1][j] + skip_penalty
                insert_score = dp[i][j-1] + insert_penalty
                
                dp[i][j] = max(match_score, skip_score, insert_score)
                
        i, j = M, N
        alignments = []
        inserted_word_list = []
        threshold = 85
        
        while i > 0 or j > 0:
            if i > 0 and j > 0:
                w_exp = clean_expected[i-1]
                w_spk = clean_spoken[j-1]
                if not w_exp or not w_spk:
                    sim = 0.0
                else:
                    sim = fuzz.ratio(w_exp, w_spk)
                    
                match_score = dp[i-1][j-1] + sim
                skip_score = dp[i-1][j] + skip_penalty
                insert_score = dp[i][j-1] + insert_penalty
                
                current = dp[i][j]
                
                if current == match_score:
                    status = "correct" if sim >= threshold else "substituted"
                    alignments.append(WordAlignmentResult(
                        index=i-1,
                        expected=words_expected[i-1],
                        spoken=words_spoken[j-1],
                        status=status,
                        similarity=sim
                    ))
                    i -= 1
                    j -= 1
                elif current == skip_score:
                    alignments.append(WordAlignmentResult(
                        index=i-1,
                        expected=words_expected[i-1],
                        spoken="",
                        status="skipped",
                        similarity=0.0
                    ))
                    i -= 1
                else:
                    inserted_word_list.append(words_spoken[j-1])
                    alignments.append(WordAlignmentResult(
                        index=i-1 if i > 0 else 0,
                        expected="",
                        spoken=words_spoken[j-1],
                        status="inserted",
                        similarity=0.0
                    ))
                    j -= 1
            elif i > 0:
                alignments.append(WordAlignmentResult(
                    index=i-1,
                    expected=words_expected[i-1],
                    spoken="",
                    status="skipped",
                    similarity=0.0
                ))
                i -= 1
            else:
                inserted_word_list.append(words_spoken[j-1])
                alignments.append(WordAlignmentResult(
                    index=0,
                    expected="",
                    spoken=words_spoken[j-1],
                    status="inserted",
                    similarity=0.0
                ))
                j -= 1
                
        alignments.reverse()
        inserted_word_list.reverse()
        
        correct_words = sum(1 for a in alignments if a.status == "correct")
        skipped_words = sum(1 for a in alignments if a.status == "skipped")
        substituted_words = sum(1 for a in alignments if a.status == "substituted")
        inserted_words = sum(1 for a in alignments if a.status == "inserted")
        
        total_words = len(words_expected)
        accuracy = (correct_words / total_words) * 100 if total_words > 0 else 0.0
        wpm = (correct_words / duration_seconds) * 60
        
        result = ReadingResult(
            accuracy=accuracy,
            wpm=wpm,
            reading_time_sec=duration_seconds,
            total_words=total_words,
            correct_words=correct_words,
            skipped_words=skipped_words,
            substituted_words=substituted_words,
            inserted_words=inserted_words,
            article_title=article_title,
            article_id=article_id,
            alignments=alignments,
            inserted_word_list=inserted_word_list,
            transcript=transcript,
            audio_path=str(audio_path)
        )
        
        # Save run to the SQLite Database
        try:
            from database.database import Database
            db = Database()
            db.insert_result(
                student_name="Guest Student",
                article_name=article_title,
                accuracy=accuracy,
                fluency=accuracy,
                pronunciation=accuracy,
                wpm=wpm,
                score=accuracy,
                total_words=total_words,
                correct_words=correct_words,
                wrong_words=skipped_words + substituted_words,
                attempts=1
            )
        except Exception:
            pass

        return result


_reading_service_instance = None


def get_reading_service() -> ReadingService:
    global _reading_service_instance
    if _reading_service_instance is None:
        _reading_service_instance = ReadingService()
    return _reading_service_instance
    
    