import os
from dataclasses import dataclass
from typing import List, Tuple, Union

import torch
from scipy.ndimage import distance_transform_edt
from torch.utils.data import Dataset
import numpy as np


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


@dataclass
class ImageToImageDataset(Dataset):
    images: List[Tuple[Union[np.ndarray, str], Union[str, np.ndarray]]]
    num_samples: int
    width: int

    def __getitem__(self, idx):
        if idx >= self.num_samples:
            raise StopIteration
        np.random.seed(idx)

        n = np.random.randint(len(self.images))
        maybe_X, maybe_Y = self.images[n]
        if isinstance(maybe_X, str):
            X = np.load(maybe_X)
        else:
            X = maybe_X
        if isinstance(maybe_Y, str):
            Y = np.load(maybe_Y)
        else:
            Y = maybe_Y

        cropped_X, cropped_Y = random_crop([X[None], Y[None]], self.width)

        return (torch.Tensor(cropped_X), torch.Tensor(cropped_Y))

    def __len__(self):
        return self.num_samples

