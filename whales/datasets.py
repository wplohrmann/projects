from functools import cache
import os
from dataclasses import dataclass, field
from typing import List, Tuple, Union
import pandas as pd

import torch
from scipy.ndimage import distance_transform_edt
from scipy.io import wavfile
from torch.utils.data import Dataset
import numpy as np
from tqdm import tqdm
from skimage.transform import resize

from detect_events import read_and_get_spectrogram as _read_and_get_spectrogram
from label import classes
from utils import get_spectrogram


def random_crop(images: List[np.ndarray], width: int, seed: int = None):
    """
    Crop a list of images of shape [..., H, W]
    All images must share the same two last dimensions.
    """
    dimensions = [x.shape[-2:] for x in images]
    # Check that dimensions is a list of identical elements
    if dimensions.count(dimensions[0]) != len(dimensions):
        raise ValueError(
            f"Images received that differ in their last two dimensions. Full shapes: {[x.shape for x in images]}"
        )
    if seed is not None:
        np.random.seed(seed)

    shape = dimensions[0]
    min_row, min_col = [np.random.randint(shape[i] - width + 1) for i in [-2, -1]]

    return [image[..., min_row : min_row + width, min_col : min_col + width] for image in images]

def tanh(x):
    pos = np.exp(x)
    neg = np.exp(-x)
    return (pos - neg) / (pos + neg)

def get_random_spectrogram(clip, samplerate, nperseg_mean, nperseg_std, shape):
    nperseg = int(np.random.normal(nperseg_mean, nperseg_std))
    _, _, image = get_spectrogram(nperseg, clip, samplerate)
    image = image.astype(np.float32)
    image = resize(image, shape)
    rescale = np.random.uniform(low=0.1, high=1.5)
    image = image + np.random.uniform(size=shape).astype(np.float32) * 0.7
    image = tanh((image / image.max()) * rescale) * 2

    return image

@dataclass
class WhaleDataset(Dataset):
    labels: pd.DataFrame
    num_samples: int
    nperseg_mean: int
    nperseg_std: int
    train: bool
    clips: List[np.ndarray] = field(default_factory=list)
    class_labels: List[np.ndarray] = field(default_factory=list)

    def __post_init__(self):
        failed = 0
        np.random.seed(0)
        print("Before split", self.labels.groupby("class_name").count()["file"])
        split_index = int(0.8 * len(self.labels))
        if self.train:
            self.labels = self.labels.sample(frac=1).iloc[:split_index]
        else:
            self.labels = self.labels.sample(frac=1).iloc[split_index:]

        print("After split", self.labels.groupby("class_name").count()["file"])
        for _, row in tqdm(self.labels.iloc[:].iterrows(), total=len(self.labels)):
            samplerate, data = wavfile.read(row["file"])
            t = np.arange(len(data)) / samplerate
            avg_t = (row["min_t"] + row["max_t"]) / 2
            # 2 seconds per clip
            min_index = np.argmin(np.abs(avg_t - 1 - t))
            max_index = np.argmin(np.abs(avg_t + 1 - t))
            if (max_index - min_index) / samplerate < 2:
                failed += 1
                continue
            self.clips.append(data[min_index:max_index])
            self.class_labels.append(row["class_name"])
        print(failed, "events were not included")
        self.samplerate = samplerate
        _, _, test_image = get_spectrogram(self.nperseg_mean, self.clips[0], samplerate)
        self.shape = test_image.shape

    def __getitem__(self, idx):
        if idx >= self.num_samples:
            raise StopIteration
        np.random.seed(idx)

        i = np.random.randint(len(self.clips))
        # TODO: Pick clips uniformly among classes
        clip = self.clips[i]

        nperseg_std = self.nperseg_std if self.train else 0
        image = get_random_spectrogram(
            clip,
            self.samplerate,
            nperseg_mean=self.nperseg_mean,
            nperseg_std=nperseg_std,
            shape=self.shape
        )
        labels = np.zeros(len(classes), dtype=np.float32)
        labels[classes.index(self.class_labels[i])] += 1


        return (torch.Tensor(image[None]), torch.Tensor(labels))

    def __len__(self):
        return self.num_samples

