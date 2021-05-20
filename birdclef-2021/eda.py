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
    return specgram, bin_width

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

def extract_template(f):
    clip, bin_width = spectrogram(f)
    clip -= clip.mean()
    distance = int(1 / bin_width)
    power = clip.sum(0)
    power[clip.shape[1]-distance//2:] = np.min(power)
    power[:distance//2] = np.min(power)

    x = np.argmax(power)
    template = np.copy(clip[:,x-distance//2:x+distance//2])
    template -= template.mean()
    template /= np.sqrt(np.sum(template**2))

    correlated = signal.correlate(clip, template, mode="valid")
    calibration = signal.correlate(clip**2, np.ones_like(template), mode="valid")
    correlated /= np.sqrt(calibration)

    peaks, properties = signal.find_peaks(correlated[0], distance=distance, prominence=0.2)

    template = np.mean([clip[:,peak:peak+distance] for peak in peaks], axis=0)

    template -= template.mean()
    template /= np.sqrt(np.sum(template**2))

    return template


metadata_path = "input/train_metadata.csv"
metadata = pd.read_csv(metadata_path)

short_audio_path = "input/train_short_audio"
all_birds = os.listdir(short_audio_path)

bird = "scptyr1"
base = os.path.join(short_audio_path, bird)

templates = []
files = metadata[metadata["primary_label"]==bird].sort_values("rating", ascending=False)["filename"] # TODO: Remove secondary label recordings
for i, f in enumerate(files):
    path = os.path.join(base, f)
    analyse(path)
    template = extract_template(path)
    plt.imshow(template)
    plt.show()

# template = find_template(templates)
# plt.imshow(template); plt.show()

for i, f in enumerate(os.listdir(base)):
    path = os.path.join(base, f)
    analyse(path)
