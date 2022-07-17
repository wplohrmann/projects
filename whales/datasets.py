from functools import cache
import os
from dataclasses import dataclass
from typing import List, Tuple, Union
import pandas as pd

import torch
from scipy.ndimage import distance_transform_edt
from torch.utils.data import Dataset
import numpy as np

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
class ImageToTimeDataset(Dataset):
    files: List[str]
    labels: pd.DataFrame
    num_samples: int
    width: int


    def __getitem__(self, idx):
        if idx >= self.num_samples:
            raise StopIteration
        np.random.seed(idx)

        while True:
            file = np.random.choice(self.files)
            m, t, spectrogram = read_and_get_spectrogram(file)
            if m is not None:
                break
        min_index = np.random.randint(spectrogram.shape[1] - self.width)
        crop = spectrogram[:, min_index:min_index+self.width]
        crop_t = t[min_index:min_index + self.width]
        labels = np.zeros((len(classes), crop.shape[1]), dtype=np.float32)
        relevant = self.labels[self.labels["file"] == file]
        for _, row in relevant.iterrows():
            labels[classes.index(row["class_name"]), np.logical_and(row["min_t"] < crop_t, crop_t < row["max_t"])] = 1


        return (torch.Tensor(crop[None]), torch.Tensor(labels))

    def __len__(self):
        return self.num_samples

