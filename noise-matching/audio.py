import pyaudio
from scipy import signal
from time import time
import numpy as np
import matplotlib.cm as cm
import wave
import streamlit as st
from multiprocessing import Queue, Process

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
MAX_WINDOW = 5 # seconds
CHUNK = int(RATE * 0.1)
NPERSEG = RATE * 20e-3 # 20ms

class Processor:
    def __enter__(self):
        self.data_queue = Queue()
        self.message_queue = Queue()
        self.process = Process(target=self.main_loop)
        self.process.start()

        return self

    def __exit__(self, *args):
        self.stop()
        self.process.join()

    def stop(self):
        self.message_queue.put("STOP")

    def get_latest(self):
        self.message_queue.put("REQUEST")
        return self.data_queue.get()

    def main_loop(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        all_data = np.array([], dtype=np.int16)
        t0 = None
        try:
            while True:
                t0 = time()
                new_samples = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
                all_data = np.concatenate([all_data, new_samples])
                all_data = all_data[-(MAX_WINDOW*RATE):]

                sample_frequencies, segment_times, stft = signal.stft(all_data, fs=RATE, nperseg=NPERSEG)
                scaled = np.log(np.abs(stft))
                if not self.message_queue.empty():
                    message = self.message_queue.get_nowait()
                    if message == "STOP":
                        return
                    if message == "REQUEST":
                        self.data_queue.put(scaled)
                print("Ran compute loop")

                print(f"Took {(time()-t0)*1000}ms to process {CHUNK/RATE*1000}ms")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
