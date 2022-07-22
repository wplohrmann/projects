from functools import cache
import os
from dataclasses import dataclass, field
from typing import List, Tuple, Union
import pandas as pd

import torch
from scipy.ndimage import distance_transform_edt
from torch.utils.data import Dataset
import numpy as np
from tqdm import tqdm

from detect_events import read_and_get_spectrogram as _read_and_get_spectrogram
from label import classes


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


@cache
def read_and_get_spectrogram(file):
    m, t, spectrogram = _read_and_get_spectrogram(file)
    if m is None:
        return None, None, None
    return m, t, spectrogram.astype(np.float32)

@dataclass
class WhaleDataset(Dataset):
    labels: pd.DataFrame
    num_samples: int
    width: int
    train: bool
    images: List[np.ndarray] = field(default_factory=list)
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
            m, t, spectrogram = read_and_get_spectrogram(row["file"])
            avg_t = (row["min_t"] + row["max_t"]) / 2
            avg_t_index = np.argmin(np.abs(avg_t - t))
            min_index = int(avg_t_index - self.width  // 2)
            max_index = int(avg_t_index + self.width // 2)
            if min_index < 0 or max_index > len(t):
                continue
            self.images.append(spectrogram[:, min_index:max_index])
            self.class_labels.append(row["class_name"])
        print(failed, "events were not included")

    def __getitem__(self, idx):
        if idx >= self.num_samples:
            raise StopIteration
        np.random.seed(idx)

        i = np.random.randint(len(self.images))
        rescale = np.random.uniform(low=0.1, high=1.5)
        image = self.images[i] + np.random.uniform(size=self.images[i].shape).astype(np.float32) * 0.7
        image = torch.Tensor(image[None])
        image = torch.tanh(image / image.max() * rescale) * 2
        labels = np.zeros(len(classes), dtype=np.float32)
        labels[classes.index(self.class_labels[i])] += 1


        return (torch.Tensor(image), torch.Tensor(labels))

    def __len__(self):
        return self.num_samples

