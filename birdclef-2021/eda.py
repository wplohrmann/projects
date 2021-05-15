import pandas as pd
import os
import soundfile as sf
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from sklearn.decomposition import PCA

def spectrogram(f):
    data, samplerate = sf.read(f)
    bin_width = 10e-3
    nperseg = int(bin_width * samplerate)
    ts, fs, specgram = signal.spectrogram(data, samplerate, nperseg=nperseg)
    specgram = np.log(specgram+1e-9)
    return specgram, 10e-3

def analyse(f):
    data, samplerate = sf.read(f)
    try:
        sd.play(data, samplerate)
        clip, bin_width = spectrogram(f)
        clip -= clip.mean()

        convolved = signal.correlate(clip, template, mode="valid")
        calibration = signal.correlate(clip**2, np.ones_like(template), mode="valid")
        convolved /= np.sqrt(calibration)

        fig, axes = plt.subplots(3, 1, sharex=True)
        axes[0].imshow(clip)
        axes[0].set_title(f)

        axes[1].plot(convolved[0])
        axes[1].set_title("Correlation")

        axes[2].plot(clip.sum(axis=0))
        axes[2].set_title("Power")
        plt.show()

    finally:
        sd.stop()

def extract_segments(f):
    clip, bin_width = spectrogram(f)
    power = clip.sum(0)
    distance = int(1 / bin_width)
    peaks, properties = signal.find_peaks(power, distance=distance)

    segments = [clip[:,x-distance//2:x+distance//2] for x in peaks if distance//2 <= x < clip.shape[1]-distance//2]

    return segments
    # plt.plot(power)
    # ylim = plt.ylim()
    # plt.vlines(peaks, *ylim)
    # plt.ylim(ylim)
    # plt.show()
def find_template(segments):
    pca = PCA(1)
    reshaped = np.stack(segments, axis=0).reshape((len(segments), -1))
    pca.fit(reshaped)
    for component in pca.components_:
        plt.imshow(component.reshape(segments[0].shape))
        plt.show()

    template = pca.components_[0].reshape(segments[0].shape)
    template -= template.mean()
    template /= np.sqrt(np.sum(template**2))

    return template




metadata_path = "input/train_metadata.csv"
metadata = pd.read_csv(metadata_path)

short_audio_path = "input/train_short_audio"
all_birds = os.listdir(short_audio_path)

bird = "pirfly1"
base = os.path.join(short_audio_path, bird)

# Plan to find a good example
# Find peaks in power(t), then grab a second chunk out of each
# Next align all the examples (max correlation), then denoise with PCA
# Also make sure to use noise examples for denoising

segments = []
for i, f in enumerate(os.listdir(base)):
    path = os.path.join(base, f)
    segments.extend(extract_segments(path))
template = find_template(segments)

for i, f in enumerate(os.listdir(base)):
    path = os.path.join(base, f)
    analyse(path)
