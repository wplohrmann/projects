import pandas as pd
import os
import soundfile as sf
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

def spectrogram(f):
    data, samplerate = sf.read(f)
    nperseg = int(10e-3 * samplerate)
    ts, fs, specgram = signal.spectrogram(data, samplerate, nperseg=nperseg)
    specgram = np.log(specgram+1e-9)
    return specgram

def analyse(f):
    data, samplerate = sf.read(f)
    try:
        sd.play(data, samplerate)
        clip = spectrogram(path)
        clip -= clip.mean()
        clip /= np.std(clip)
        convolved = signal.correlate(clip, sound, mode="valid")

        plt.subplot(211)
        plt.imshow(clip)
        plt.title(f)

        plt.subplot(212)
        plt.plot(convolved[0])
        plt.show()

    finally:
        sd.stop()


metadata_path = "input/train_metadata.csv"
metadata = pd.read_csv(metadata_path)

short_audio_path = "input/train_short_audio"
all_birds = os.listdir(short_audio_path)

bird = "pirfly1"
base = os.path.join(short_audio_path, bird)

sound = spectrogram(os.path.join(base, os.listdir(base)[0]))[:,150:250]
sound -= sound.mean()
sound /= np.std(sound)

for i, f in enumerate(os.listdir(base)):
    path = os.path.join(base, f)
    analyse(os.path.join(base, f))
