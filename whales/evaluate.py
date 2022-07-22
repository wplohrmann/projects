from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import torch
from torchmetrics import ConfusionMatrix
from datasets import WhaleDataset

from utils import get_resnet18, classes


labels = pd.read_csv("labels.csv")
num_classes = len(classes)
model = get_resnet18(num_classes, model_path="model.pt")
model.eval()

for train in [True, False]:
    if train:
        print("Evaluation on train-dataset")
    else:
        print("Evaluation on val-dataset")
    dataset = WhaleDataset(labels, 1, width=64, train=train)
    confusion_matrix = ConfusionMatrix(num_classes)
    for image, class_name in zip(dataset.images, dataset.class_labels):
        with torch.no_grad():
            pred = model(torch.tensor(image[None, None] / image.max()))
        class_pred = torch.argmax(pred, dim=1)
        Y = torch.tensor([classes.index(class_name)])
        confusion_matrix.update(class_pred, Y)

    matrix = confusion_matrix.compute()

    fig, ax = plt.subplots(1, 1)
    ax.imshow(matrix)
    ax.set_xticks(np.arange(num_classes))
    ax.set_yticks(np.arange(num_classes))
    ax.set_xticklabels(classes)
    ax.set_yticklabels(classes)
    ax.set_ylabel("Ground truth")
    ax.set_xlabel("Prediction")
    ax.set_title("Confusion matrix")
    for (i, j), z in np.ndenumerate(matrix.numpy()):
        ax.text(j, i, str(z), ha="center", va="center")
    plt.show()

    accuracy = (torch.trace(matrix) / torch.sum(matrix)).item()
    print(f"Total accuracy: {accuracy*100:.2f}%")
    for i, class_name in enumerate(classes):
        class_accuracy = matrix[i, i] / torch.sum(matrix[i])
        print(f"Recall '{class_name}': {class_accuracy*100:.2f}%")
