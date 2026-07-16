"""
==========================================================
ReadingAI Speech Engine
Whisper Based Speech Recognition Engine
==========================================================
"""

import os
import queue
import tempfile
import threading
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
import whisper

from config import (
    CACHE_DIR,
    WHISPER_MODEL,
)

from utils.logger import (
    info,
    warning,
    error,
)


class SpeechEngine:

    def __init__(self):
        self.device = self.detect_device()
        self.model = None
        self.model_loaded = False
        self.sample_rate = 16000
        self.language = "en"
        self.audio_queue = queue.Queue()
        self.transcript = ""
        self.is_recording = False
        self.thread = None
        self.lock = threading.Lock()
        self.load_model()

    def detect_device(self):
        if torch.cuda.is_available():
            info("CUDA Available")
            info(torch.cuda.get_device_name(0))
            return "cuda"
        warning("CUDA Not Available")
        return "cpu"

    def load_model(self):
        try:
            info("Loading Whisper Model")
            self.model = whisper.load_model(
                WHISPER_MODEL,
                device=self.device,
                download_root=str(CACHE_DIR)
            )
            self.model_loaded = True
            info("Whisper Loaded Successfully")
        except Exception as e:
            error(str(e))
            raise RuntimeError("Unable to Load Whisper")

    def is_ready(self):
        return self.model_loaded

    def model_name(self):
        return WHISPER_MODEL

    def current_device(self):
        return self.device

    def save_audio(self, audio, sample_rate=None):
        if sample_rate is None:
            sample_rate = self.sample_rate
        temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(temp.name, audio, sample_rate)
        return temp.name

    def load_audio(self, file_path):
        audio, sr = sf.read(file_path)
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        return audio, sr

    def normalize(self, audio):
        audio = np.asarray(audio, dtype=np.float32)
        maximum = np.max(np.abs(audio))
        if maximum == 0:
            return audio
        return audio / maximum

    def duration(self, audio):
        return len(audio) / self.sample_rate

    def empty(self, audio):
        return len(audio) == 0

    def energy(self, audio):
        return float(np.mean(np.square(audio)))

    def silence(self, audio, threshold=0.0005):
        return self.energy(audio) < threshold

    def valid_audio(self, audio):
        if self.empty(audio):
            return False
        if self.silence(audio):
            return False
        return True

    def remove(self, file_path):
        try:
            os.remove(file_path)
        except:
            pass

    def transcribe(self, audio):
        if not self.valid_audio(audio):
            return ""
        file_path = self.save_audio(audio)
        try:
            result = self.model.transcribe(
                file_path,
                language=self.language,
                fp16=(self.device == "cuda"),
                verbose=False
            )
            text = result["text"].strip()
            self.remove(file_path)
            return text
        except Exception as e:
            self.remove(file_path)
            error(str(e))
            return ""

    def transcribe_file(self, file_path):
        try:
            result = self.model.transcribe(
                file_path,
                language=self.language,
                fp16=(self.device == "cuda"),
                verbose=False
            )
            return result["text"].strip()
        except Exception as e:
            error(str(e))
            return ""

    def full_result(self, file_path):
        try:
            return self.model.transcribe(
                file_path,
                language=self.language,
                fp16=(self.device == "cuda"),
                verbose=False
            )
        except Exception as e:
            error(str(e))
            return {}

    def segments(self, file_path):
        result = self.full_result(file_path)
        if result == {}:
            return []
        return result.get("segments", [])

    def set_language(self, language):
        self.language = language

    def get_language(self):
        return self.language

    def clear(self):
        self.transcript = ""

    def last_text(self):
        return self.transcript

    def start_recording(self):
        self.is_recording = True
        self.clear()
        while not self.audio_queue.empty():
            self.audio_queue.get()
        info("Recording Started")

    def stop_recording(self):
        self.is_recording = False
        info("Recording Stopped")

    def recording(self):
        return self.is_recording

    def push_audio(self, audio):
        if not self.is_recording:
            return
        self.audio_queue.put(audio)

    def has_audio(self):
        return not self.audio_queue.empty()

    def pop_audio(self):
        if self.audio_queue.empty():
            return None
        return self.audio_queue.get()

    def clear_buffer(self):
        while not self.audio_queue.empty():
            self.audio_queue.get()

    def buffer_size(self):
        return self.audio_queue.qsize()

    def process_next_audio(self):
        if not self.has_audio():
            return ""
        audio = self.pop_audio()
        if audio is None:
            return ""
        text = self.transcribe(audio)
        with self.lock:
            self.transcript = text
        return text

    def current_text(self):
        with self.lock:
            return self.transcript

    def append_text(self, text):
        if text.strip() == "":
            return
        with self.lock:
            if self.transcript == "":
                self.transcript = text
            else:
                self.transcript += " " + text

    def reset(self):
        self.stop_recording()
        self.clear()
        self.clear_buffer()

    def tokenize(self, text):
        return [word.strip() for word in text.split() if word.strip() != ""]

    def current_spoken_word(self, transcript):
        words = self.tokenize(transcript)
        if len(words) == 0:
            return ""
        return words[-1]

    def expected_word(self, session):
        return session.current_word()

    def match_word(self, session, aligner):
        expected = self.expected_word(session)
        spoken = self.current_spoken_word(self.current_text())
        if expected is None:
            return {"status": "completed"}
        result = aligner.compare(expected, spoken)
        return result

    def check_current_word(self, session, aligner):
        result = self.match_word(session, aligner)
        if result.get("status") == "completed":
            return result
        if result["correct"]:
            session.add_spoken_word(result["spoken"])
            session.next_word()
        else:
            session.add_error(result["spoken"])
            session.increase_attempt()
        return result

    def attempts(self, session):
        return session.current_attempt()

    def allow_next(self, session, aligner):
        result = self.match_word(session, aligner)
        return result["correct"]

    def live_result(self, session, aligner):
        result = self.check_current_word(session, aligner)
        return {
            "expected": session.current_word(),
            "spoken": result.get("spoken", ""),
            "correct": result.get("correct", False),
            "similarity": result.get("similarity", 0),
            "attempts": session.current_attempt()
        }

    def current_status(self, session, aligner, hint_engine):
        result = self.match_word(session, aligner)
        attempts = session.current_attempt()
        hint = hint_engine.build_hint(session.current_word(), attempts)
        return {
            "expected": session.current_word(),
            "spoken": result.get("spoken", ""),
            "correct": result.get("correct", False),
            "similarity": result.get("similarity", 0),
            "attempts": attempts,
            "hint": hint
        }

    def word_color(self, correct):
        if correct:
            return "#16a34a"
        return "#dc2626"

    def highlight_word(self, word, correct):
        color = self.word_color(correct)
        return f'<span style="color:{color};font-size:28px;font-weight:bold;">{word}</span>'

    def locked_word(self, word):
        return f'<span style="color:#9ca3af;font-size:28px;font-weight:bold;">{word}</span>'

    def build_article(self, session, aligner):
        html = ""
        current = session.current_index
        spoken = self.current_spoken_word(self.current_text())
        for index, word in enumerate(session.words):
            if index < current:
                html += self.highlight_word(word, True) + " "
            elif index == current:
                ok = aligner.is_correct(word, spoken)
                html += self.highlight_word(word, ok) + " "
            else:
                html += self.locked_word(word) + " "
        return html

    def completed(self, session):
        return session.completed

    def reset_current_word(self):
        self.clear()

    def live_loop(self, session, aligner, hint_engine, scorer):
        while self.is_recording:
            if not self.has_audio():
                continue
            text = self.process_next_audio()
            if text == "":
                continue
            result = self.check_current_word(session, aligner)
            if result.get("correct", False):
                scorer.add_correct()
                self.clear()
            else:
                scorer.add_wrong()
            if self.completed(session):
                scorer.stop()
                session.accuracy = scorer.accuracy()
                session.fluency = scorer.fluency()
                session.wpm = scorer.words_per_minute()
                session.score = scorer.final_score()
                self.stop_recording()
                break

    def start_engine(self, session, aligner, hint_engine, scorer):
        if self.thread is not None:
            if self.thread.is_alive():
                return
        scorer.start()
        self.start_recording()
        self.thread = threading.Thread(
            target=self.live_loop,
            args=(session, aligner, hint_engine, scorer),
            daemon=True
        )
        self.thread.start()

    def stop_engine(self):
        self.stop_recording()
        if self.thread:
            self.thread.join(timeout=1)

    def engine_running(self):
        if self.thread is None:
            return False
        return self.thread.is_alive()

    def ui_data(self, session, aligner, hint_engine, scorer):
        result = self.current_status(session, aligner, hint_engine)
        return {
            "article_html": self.build_article(session, aligner),
            "transcript": self.current_text(),
            "current_word": session.current_word(),
            "attempts": result["attempts"],
            "hint": result["hint"],
            "accuracy": scorer.accuracy(),
            "fluency": scorer.fluency(),
            "wpm": scorer.words_per_minute(),
            "score": scorer.final_score(),
            "completed": session.completed
        }

    def close(self):
        self.stop_engine()
        self.clear()
        self.clear_buffer()
        self.model = None
        self.model_loaded = False