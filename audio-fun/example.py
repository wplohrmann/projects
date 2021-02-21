import pyaudio
from time import time
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import wave
 
WAVE_OUTPUT_FILENAME = "file.wav"
RECORD_SECONDS = 10
from audio import FORMAT, CHANNELS, RATE, CHUNK
 
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print("recording...")
chunks = []
 
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    chunk = stream.read(CHUNK)
    chunks.append(chunk)
print("finished recording")
data = np.concatenate([np.frombuffer(chunk, dtype=np.int16) for chunk in chunks])
 
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
if True:
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(data)
    waveFile.close()
