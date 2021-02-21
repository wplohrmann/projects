import pyaudio
from time import time
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import wave
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
 
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print("recording...")
frames = []
 
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("finished recording")
arr = np.concatenate([np.frombuffer(frame, dtype=np.int16) for frame in frames])
 
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
if True:
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(arr)
    waveFile.close()

nperseg = RATE * 20e-3 # 20ms
sample_frequencies, segment_times, stft = signal.stft(arr, fs=RATE, nperseg=RATE*20e-3)
sample_frequencies /= 1000 # Hz -> kHz

plt.imshow(np.log(np.abs(stft)), interpolation="none", extent=[segment_times[0], segment_times[-1], sample_frequencies[0], sample_frequencies[-1]], aspect="auto")
plt.title("STFT Magnitude")
plt.ylabel("Frequency [kHz]")
plt.xlabel("Time [sec]")
plt.show()
