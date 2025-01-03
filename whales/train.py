import argparse
import os
import numpy as np
import pandas as pd

from scipy.io import wavfile
import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader
from torch import nn
from tqdm import tqdm


from utils import get_resnet18
from datasets import Repeater, WhaleDataset
from label import classes

parser = argparse.ArgumentParser(description="Train or evaluate a model on marine mammal detection")
parser.add_argument("--skip-training", action="store_true")
args = parser.parse_args()


labels = pd.read_csv("labels.csv")

if args.skip_training:
    model = get_resnet18(len(classes), model_path="model.pt")
else:
    batch_size = 32
    learning_rate = 1e-3
    num_samples = 50000
    num_repeats = 20
    cache_size = 200

    dataset = WhaleDataset(labels, num_samples, train=True, nperseg_mean=2048, nperseg_std=500)
    model = get_resnet18(len(classes))
    model.train()

    repeater = Repeater(dataset, num_repeats, cache_size)
    data_loader = DataLoader(repeater, batch_size=batch_size, shuffle=True)
    loss_fn = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    pbar = tqdm(data_loader)
    try:
        for X, Y in pbar:
            if False:
                plt.imshow(X[0, 0])
                plt.title(classes[np.argmax(Y[0])])
                plt.show()
                continue
            pred = torch.sigmoid(model(X))
            loss = loss_fn(pred, Y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            loss = loss.item()
            pbar.set_description(f"loss: {loss:>7f}")
    except KeyboardInterrupt:
        pass

    torch.save(model.state_dict(), "model.pt")
