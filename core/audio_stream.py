"""
==========================================================
ReadingAI

Live Audio Stream Engine

Author : Vishal Kumar

==========================================================
"""

import queue
import threading

import av
import numpy as np

from streamlit_webrtc import AudioProcessorBase


class AudioBuffer:

    """
    Thread Safe Audio Queue
    """

    def __init__(self):

        self.queue = queue.Queue()

        self.lock = threading.Lock()

    # ============================================

    def put(self, audio):

        with self.lock:

            self.queue.put(audio)

    # ============================================

    def get(self):

        if self.queue.empty():

            return None

        with self.lock:

            return self.queue.get()

    # ============================================

    def empty(self):

        return self.queue.empty()

    # ============================================

    def clear(self):

        while not self.queue.empty():

            self.queue.get()

    # ============================================

    def size(self):

        return self.queue.qsize()


audio_buffer = AudioBuffer()


class AudioProcessor(AudioProcessorBase):

    """
    Receives Live Audio

    Browser

            ↓

    Streamlit

            ↓

    Queue

    """

    def recv(

        self,

        frame: av.AudioFrame

    ):

        audio = frame.to_ndarray()

        audio = audio.astype(

            np.float32

        )

        audio = audio.flatten()

        audio_buffer.put(audio)

        return frame
    import time
import numpy as np


class AudioStream:

    """
    Live Audio Processing Engine
    """

    def __init__(self):

        self.sample_rate = 16000

        self.chunk_duration = 2

        self.samples_per_chunk = (

            self.sample_rate *

            self.chunk_duration

        )

        self.energy_threshold = 0.0005

        self.max_buffer = []

    # =====================================================
    # AUDIO ENERGY
    # =====================================================

    def energy(

        self,

        audio

    ):

        if len(audio) == 0:

            return 0

        return float(

            np.mean(

                np.square(audio)

            )

        )

    # =====================================================
    # SILENCE
    # =====================================================

    def silence(

        self,

        audio

    ):

        return (

            self.energy(audio)

            <

            self.energy_threshold

        )

    # =====================================================
    # NORMALIZE
    # =====================================================

    def normalize(

        self,

        audio

    ):

        if len(audio) == 0:

            return audio

        maximum = np.max(

            np.abs(audio)

        )

        if maximum == 0:

            return audio

        return audio / maximum

    # =====================================================
    # ADD BUFFER
    # =====================================================

    def add(

        self,

        audio

    ):

        self.max_buffer.extend(

            audio.tolist()

        )

    # =====================================================
    # BUFFER READY
    # =====================================================

    def ready(self):

        return (

            len(self.max_buffer)

            >=

            self.samples_per_chunk

        )

    # =====================================================
    # NEXT BUFFER
    # =====================================================

    def next_chunk(self):

        if not self.ready():

            return None

        audio = np.array(

            self.max_buffer[

                :self.samples_per_chunk

            ],

            dtype=np.float32

        )

        self.max_buffer = self.max_buffer[

            self.samples_per_chunk:

        ]

        audio = self.normalize(audio)

        return audio

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        self.max_buffer = []

    # =====================================================
    # WAIT FOR AUDIO
    # =====================================================

    def collect(self):

        while True:

            if audio_buffer.empty():

                time.sleep(

                    0.01

                )

                continue

            frame = audio_buffer.get()

            self.add(frame)

            if self.ready():

                chunk = self.next_chunk()

                if chunk is None:

                    continue

                if self.silence(chunk):

                    continue

                return chunk
            