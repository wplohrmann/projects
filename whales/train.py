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


from utils import Model
from datasets import ImageToTimeDataset
from label import classes

parser = argparse.ArgumentParser(description="Train or evaluate a model on marine mammal detection")
parser.add_argument("--skip-training", action="store_true")
args = parser.parse_args()


files = []
for dir_name in tqdm(os.listdir("data")):
    if not dir_name.endswith("converted"):
        continue
    dir = os.path.join("data", dir_name)
    for filename in tqdm(os.listdir(dir)):
        files.append(os.path.join(dir, filename))

# nperseg = 3000 # Try training on multiple different settings
np.random.seed(0)
image_pairs = []
if args.skip_training:
    n_spectrograms = 0
else:
    n_spectrograms = 20

labels = pd.read_csv("labels.csv")

if args.skip_training:
    model = Model(model_path="model.pt")
else:
    batch_size = 32
    learning_rate = 1e-3
    num_samples = 200000

    dataset = ImageToTimeDataset(files, labels, num_samples, width=64)
    model = Model()
    model.train()

    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    loss_fn = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    pbar = tqdm(data_loader)
    for X, Y in pbar:
        pred = model(X)
        loss = loss_fn(pred, Y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        loss = loss.item()
        pbar.set_description(f"loss: {loss:>7f}")

    torch.save(model.state_dict(), "model.pt")

# for pair in pairs:
#     samplerate, data = wavfile.read(os.path.join("data", pair[1]))
#     df = pd.read_csv(os.path.join("data", pair[0]))

#     nperseg = 3000
#     f, t, spectrogram = get_spectrogram(nperseg, data, samplerate)
#     labels = get_labels(df, spectrogram.shape, f, t)
#     cropped = spectrogram[None, None, :, :-(spectrogram.shape[1]%16)]
#     model.eval()

#     with torch.no_grad():
#         pred = model(torch.as_tensor(cropped))[0]

#     fig, axes = plt.subplots(len(classes), 2, sharex=True, sharey=True)
#     for i, class_name in enumerate(classes):
#         axes[i, 0].imshow(pred[i], aspect="auto")
#         axes[i, 0].set_title(f"Prediction {class_name}")
#         axes[i, 1].imshow(labels[i], aspect="auto")
#         axes[i, 1].set_title(f"Ground truth {class_name}")
#     plt.show()
#
