from typing import List
import numpy as np
import torch

from datasets import WhaleDataset, get_random_spectrogram


class BarlowModel(torch.nn.Module):
    def __init__(self, base_model, embedding_dim, dim1: int, dim2: int):
        super().__init__()
        self.base_model = base_model
        self.dim1 = dim1
        self.dim2 = dim2
        self.fc1 = torch.nn.Linear(in_features=embedding_dim, out_features=dim1)
        self.fc2 = torch.nn.Linear(in_features=dim1, out_features=dim2)
        self.relu = torch.nn.ReLU()

    def forward(self, x):
        x = self.base_model(x)
        x = self.relu(x)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)

        return x

    def embed(self, x):
        return self.base_model(x)

class WhalePairs(WhaleDataset):
    def __getitem__(self, idx):
        if idx >= self.num_samples:
            raise StopIteration
        np.random.seed(idx)

        i = np.random.choice(len(self.clips), p=self.p)
        clip = self.clips[i]

        nperseg_std = self.nperseg_std if self.train else 0
        image1 = get_random_spectrogram(
            clip,
            self.samplerate,
            nperseg_mean=self.nperseg_mean,
            nperseg_std=nperseg_std,
            shape=self.shape
        )

        image2 = get_random_spectrogram(
            clip,
            self.samplerate,
            nperseg_mean=self.nperseg_mean,
            nperseg_std=nperseg_std,
            shape=self.shape
        )


        return (torch.Tensor(image1[None]), torch.Tensor(image2[None]))


class BarlowLoss:
    def __init__(self, lamda, dims):
        self.lamda = lamda
        self.dims = dims
        self.weights = torch.eye(dims) + (torch.ones((dims, dims)) - torch.eye(dims)) * self.lamda

    def __call__(self, embedding_1, embedding_2):
        cc = self.get_cc(embedding_1, embedding_2)
        cc_diff: torch.Tensor = (cc - torch.eye(self.dims)).pow(2)
        cc_diff *= self.weights

        return torch.mean(cc_diff)

    def get_cc(self, embedding_1, embedding_2):
        N, D = embedding_1.shape
        assert embedding_2.shape == (N, D)
        norm_1 = (embedding_1 - embedding_1.mean(dim=0)) / torch.std(embedding_1, dim=0, keepdim=True)
        norm_2 = (embedding_2 - embedding_2.mean(dim=0)) / torch.std(embedding_2, dim=0, keepdim=True)
        return torch.mm(norm_1.T, norm_2) / N
