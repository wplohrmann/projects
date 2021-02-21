import pyaudio
from time import time
from scipy import signal
import numpy as np
import matplotlib.cm as cm
import wave
import streamlit as st

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
MAX_WINDOW = 5 # seconds
CHUNK = int(RATE * 0.1)

st.title("Noise matching")

start_recording = st.button("Start recording")
stop_recording = st.button("Stop recording")

spectrogram = None

if start_recording:
    frames = []
    audio = pyaudio.PyAudio()
    try:
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        offset = 0
        while True:
            data = stream.read(CHUNK)
            t0 = time()
            if len(frames) == MAX_WINDOW * RATE // CHUNK:
                frames.pop(0)
                offset += CHUNK / RATE
            frames.append(data)

            arr = np.concatenate([np.frombuffer(frame, dtype=np.int16) for frame in frames])
            nperseg = RATE * 20e-3 # 20ms
            sample_frequencies, segment_times, stft = signal.stft(arr, fs=RATE, nperseg=nperseg)
            t_min = segment_times[0] + offset
            t_max = segment_times[-1] + offset
            f_min = sample_frequencies[0] / 1000
            f_max = sample_frequencies[-1] / 100
            scaled = np.log(np.abs(stft))
            scaled = (scaled - scaled.min()) / (scaled.max() - scaled.min())
            image_array = cm.viridis(scaled)
            print(f"Took {(time()-t0)*1000}ms to process {CHUNK/RATE*1000}ms")

            if spectrogram is None:
                spectrogram = st.image(image_array)
            else:
                spectrogram.image(image_array)
            print(f"Took {(time()-t0)*1000}ms to process and plot {CHUNK/RATE*1000}s")


    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
