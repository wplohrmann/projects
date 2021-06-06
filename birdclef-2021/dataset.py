import os

import sounddevice as sd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch.utils.data import Dataset
import soundfile as sf
from scipy import signal

def spectrogram(f):
    data, samplerate = sf.read(f)
    bin_width = 10e-3
    nperseg = int(bin_width * samplerate)
    ts, fs, specgram = signal.spectrogram(data, samplerate, nperseg=nperseg)
    specgram = np.log(specgram+1e-9)
    return specgram, bin_width

class TrainShortAudio(Dataset):
    def __init__(self, data_dir, metadata_path, species_subset=None):
        self.data_dir = data_dir
        self.all_birds = os.listdir(data_dir)
        self.metadata = pd.read_csv(metadata_path)
        if species_subset is not None:
            self.metadata = self.metadata[self.metadata["primary_label"].isin(species_subset)]
        self.species = {species:i for i, species in enumerate(self.metadata["primary_label"].unique())}

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx, debug=False):
        row = self.metadata.iloc[idx]
        path_to_recording = os.path.join(self.data_dir, row["primary_label"], row["filename"])
        specgram, bin_width = spectrogram(path_to_recording)
        if debug:
            data, samplerate = sf.read(path_to_recording)
            try:
                sd.play(data, samplerate)
                plt.imshow(specgram)
                plt.show()
            finally:
                sd.stop()
            return path_to_recording
        label = torch.zeros(len(self.species)).scatter_(dim=0, index=torch.tensor(self.species[row["primary_label"]]), value=1)
        return torch.tensor(specgram[np.newaxis,np.newaxis,:,:]), label
