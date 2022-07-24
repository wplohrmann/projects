from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import torch
from tqdm import tqdm
from datasets import WhaleDataset, get_random_spectrogram

from utils import get_resnet18, classes, ConfusionMatrix


labels = pd.read_csv("labels.csv")
num_classes = len(classes)
model = get_resnet18(num_classes, model_path="model.pt")
model.eval()

for train in [True, False]:
    if train:
        print("Evaluation on train-dataset")
    else:
        print("Evaluation on val-dataset")
    dataset = WhaleDataset(labels, 1, train=train, nperseg_mean=2048, nperseg_std=None)
    confusion_matrix = ConfusionMatrix(classes)
    for clip, class_name in tqdm(zip(dataset.clips, dataset.class_labels), total=len(dataset.clips)):
        image = get_random_spectrogram(clip, dataset.samplerate, nperseg_mean=2048, nperseg_std=0, shape=dataset.shape, add_noise=False)
        with torch.no_grad():
            pred = model(torch.tensor(image[None, None] / image.max()))
        class_pred = torch.argmax(pred, dim=1)
        Y = torch.tensor([classes.index(class_name)])
        confusion_matrix.update(class_pred, Y)

    confusion_matrix.plot()
