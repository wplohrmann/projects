from collections import defaultdict
import os
import numpy as np
import pandas as pd

from scipy.io import wavfile
import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader
from torch import nn
from tqdm import tqdm


from utils import get_model, get_spectrogram
from datasets import ImageToImageDataset

pairs = ("Up_call_EOS_220405_095834.csv", "Up_call_EOS_220405_095834.wav")


samplerate, data = wavfile.read(os.path.join("data", pairs[1]))

nperseg = 3000
f, t, spectrogram = get_spectrogram(nperseg, data, samplerate)

gray = np.stack([spectrogram for _ in range(3)], axis=-1)

df = pd.read_csv(os.path.join("data", pairs[0]))
labels = np.zeros(spectrogram.shape)
df["cols"] = np.argmin(np.abs(df["t / s"].values[:, None] - t[None, :]), axis=1)
df["rows"] = np.argmin(np.abs(df["f / Hz"].values[:, None] - f[None, :]), axis=1)

labels[df["rows"], df["cols"]] = 1

plt.imshow(gray, aspect="auto")
plt.scatter(df["cols"], df["rows"])
plt.show()


batch_size = 1
learning_rate = 1e-3
num_samples = 500
train_index = labels.shape[1] // 2

dataset = ImageToImageDataset([(spectrogram[:, :train_index], labels[:, :train_index])], num_samples, width=64)
model = get_model(8, ('mateuszbuda/brain-segmentation-pytorch', 'unet'), 1)
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

cropped = spectrogram[None, None, :, :-(spectrogram.shape[1]%16)]
model.eval()
with torch.no_grad():
    pred = model(torch.as_tensor(cropped))[0, 0]

fig, axes = plt.subplots(2, 1, sharex=True, sharey=True)
axes[0].imshow(pred, aspect="auto")
axes[0].set_title("prediction")
axes[1].imshow(labels, aspect="auto")
axes[1].set_title("labels")
plt.show()
