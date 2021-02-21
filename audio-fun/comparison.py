import wave
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

from audio import RATE, NPERSEG

def open_wav(path):
    with wave.open(path) as handle:
        nchannels, sampwidth, framerate, nframes, comptype, compname = handle.getparams()
        data = np.frombuffer(handle.readframes(nframes), dtype=np.int16)
        sample_frequencies, segment_times, stft = signal.stft(data, fs=RATE, nperseg=NPERSEG)
        scaled = np.abs(stft)
    return segment_times, sample_frequencies, scaled

bell_times, frequencies, bell = open_wav("./meet_join.wav")
background_times, _, with_background = open_wav("./meet_join_with_background.wav")

correlation = signal.correlate(with_background - with_background.mean(), bell - bell.mean(), mode="valid")
# correlation /= signal.correlate(with_background, np.ones_like(bell), mode="valid")
correlation = np.squeeze(correlation)
t = background_times[:1-bell.shape[1]]


# Plots
plt.imshow(np.log(bell), aspect="auto", extent=[bell_times[0], bell_times[-1], frequencies[0], frequencies[-1]])
plt.title("Bell")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.show()


plt.subplot(211)
plt.imshow(np.log(with_background), aspect="auto", extent=[background_times[0], background_times[-1], frequencies[0], frequencies[-1]])
plt.title("Recording with bell and background noise")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
xlim = plt.xlim()

plt.subplot(212)
plt.plot(t, correlation)
plt.title("Correlation of bell spectrogram against recording")
plt.xlabel("Time (s)")
plt.ylabel("Correlation")
plt.xlim(xlim)
plt.show()


