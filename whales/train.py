import os
import numpy as np
import pandas as pd

from scipy.io import wavfile
import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader
from torch import nn
from tqdm import tqdm


from utils import get_model, get_spectrogram, classes
from datasets import ImageToImageDataset

pairs = [
    ("Up_call_EOS_220405_095834.csv", "Up_call_EOS_220405_095834.wav"),
    ("Humpbacks_EOS_220405_133638.csv", "Humpbacks_EOS_220405_133638.wav")
]

def get_labels(df, shape, f, t):
    labels = np.zeros((len(classes),) + shape)
    class_labels = {key: i for i, key in enumerate(classes)}
    df["cols"] = np.argmin(np.abs(df["t / s"].values[:, None] - t[None, :]), axis=1)
    df["rows"] = np.argmin(np.abs(df["f / Hz"].values[:, None] - f[None, :]), axis=1)
    labels[df["Class"].apply(class_labels.__getitem__), df["rows"], df["cols"]] = 1

    return labels



# nperseg = 3000 # Try training on multiple different settings
np.random.seed(0)
image_pairs = []
for pair in pairs:
    samplerate, data = wavfile.read(os.path.join("data", pair[1]))
    df = pd.read_csv(os.path.join("data", pair[0]))

    for i in range(20):
        nperseg = np.random.randint(2500, 3500)
        f, t, spectrogram = get_spectrogram(nperseg, data, samplerate)
        labels = get_labels(df, spectrogram.shape, f, t)

        train_index = labels.shape[2] // 2
        image_pairs.append((spectrogram[..., :train_index], labels[..., :train_index]))

        if False:
            gray = np.stack([spectrogram for _ in range(3)], axis=-1)
            plt.imshow(gray, aspect="auto")
            for class_name, rows in df.groupby("Class"):
                if len(rows) > 0:
                    plt.scatter(rows["cols"], rows["rows"], label=class_name)
            plt.legend()
            plt.show()


batch_size = 32
learning_rate = 1e-3
num_samples = 50000

dataset = ImageToImageDataset(image_pairs, num_samples, width=64)
model = get_model(8, ('mateuszbuda/brain-segmentation-pytorch', 'unet'), 5)
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

for pair in pairs:
    samplerate, data = wavfile.read(os.path.join("data", pair[1]))
    df = pd.read_csv(os.path.join("data", pair[0]))

    nperseg = 3000
    f, t, spectrogram = get_spectrogram(nperseg, data, samplerate)
    labels = get_labels(df, spectrogram.shape, f, t)
    cropped = spectrogram[None, None, :, :-(spectrogram.shape[1]%16)]
    model.eval()

    with torch.no_grad():
        pred = model(torch.as_tensor(cropped))[0]

    fig, axes = plt.subplots(len(classes), 2, sharex=True, sharey=True)
    for i, class_name in enumerate(classes):
        axes[i, 0].imshow(pred[i], aspect="auto")
        axes[i, 0].set_title(f"Prediction {class_name}")
        axes[i, 1].imshow(labels[i], aspect="auto")
        axes[i, 1].set_title(f"Ground truth {class_name}")
    plt.show()
