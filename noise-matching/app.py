import pyaudio
from time import time
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import wave
import streamlit as st

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
MAX_WINDOW = 5 # seconds
CHUNK = RATE // 2

st.title("Noise matching")

clicked = st.button("Start recording")

spectrogram = None

if clicked:
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
            print(f"Took {(time()-t0)*1000}ms to process 5s")

            if spectrogram is None:
                fig = plt.figure()
                spectrogram = plt.imshow(np.log(np.abs(stft)), interpolation="none", aspect="auto",
                        extent=[t_min, t_max, f_max, f_min])
                plt.title("STFT Magnitude")
                plt.ylabel("Frequency [kHz]")
                plt.xlabel("Time [sec]")
                the_plot = st.pyplot(fig)
            else:
                spectrogram.set_data(np.log(np.abs(stft)))
                spectrogram.set_extent([t_min, t_max, f_max, f_min])
                the_plot.pyplot(plt)
            print(f"Took {(time()-t0)*1000}ms to process and plot 0.5s")


    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
