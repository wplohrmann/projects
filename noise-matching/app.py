from time import time, sleep
import numpy as np
import matplotlib.cm as cm
import wave
import streamlit as st

from audio import Processor


st.title("Noise matching")

# file_to_match = st.file_uploader(".wav file with noise to match")
# if file_to_match:
#     with wave.open(file_to_match) as handle:
#         nchannels, sampwidth, framerate, nframes, comptype, compname = handle.getparams()
#         data = np.frombuffer(handle.readframes(nframes), dtype=np.int16)
#         sample_frequencies, segment_times, stft = signal.stft(data, fs=RATE, nperseg=NPERSEG)
#         scaled = np.log(np.abs(stft))
#         scaled = (scaled - scaled.min()) / (scaled.max() - scaled.min())
#         image_array = cm.viridis(scaled)
#         st.image(image_array)
#     start_recording = st.button("Start recording")
# else:
#     start_recording = None
start_recording = st.button("Start recording")

spectrogram = None

if start_recording:
    with Processor() as processor:
        while True:
            data = processor.get_latest()
            scaled = (data - data.min()) / (data.max() - data.min())
            image_array = cm.viridis(scaled)
            if spectrogram is None:
                spectrogram = st.image(image_array)
            else:
                spectrogram.image(image_array)
            print("Ran render loop")
            sleep(0.5)
