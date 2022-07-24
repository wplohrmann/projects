"""
# Inspired by and shamelessly stolen from
# https://github.com/wvangansbeke/Unsupervised-Classification/blob/master/losses/losses.py
"""

from collections import Counter
from itertools import permutations
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import torch
from torch.nn import functional as F
from tqdm import tqdm
from barlow_twins import BarlowModel
from datasets import WhaleDataset, get_random_spectrogram
from sklearn.decomposition import PCA
from sklearn.neighbors import KDTree
from utils import ConfusionMatrix, classes, get_resnet18

EPS=1e-8

def entropy(x, input_as_probabilities):
    """
    Helper function to compute the entropy over the batch
    input: batch w/ shape [b, num_classes]
    output: entropy value [is ideally -log(num_classes)]
    """

    if input_as_probabilities:
        x_ =  torch.clamp(x, min = EPS)
        b =  x_ * torch.log(x_)
    else:
        b = F.softmax(x, dim = 1) * F.log_softmax(x, dim = 1)

    if len(b.size()) == 2: # Sample-wise entropy
        return -b.sum(dim = 1).mean()
    elif len(b.size()) == 1: # Distribution-wise entropy
        return - b.sum()
    else:
        raise ValueError('Input tensor is %d-Dimensional' %(len(b.size())))

class SCANLoss(torch.nn.Module):
    def __init__(self, entropy_weight = 2.0):
        super(SCANLoss, self).__init__()
        self.softmax = torch.nn.Softmax(dim = 1)
        self.bce = torch.nn.BCELoss()
        self.entropy_weight = entropy_weight

    def forward(self, anchors, neighbors):
        """
        input:
            - anchors: logits for anchor images w/ shape [b, num_classes]
            - neighbors: logits for neighbor images w/ shape [b, num_classes]
        output:
            - Loss
        """
        b, n = anchors.size()
        # Similarity in output space
        similarity = torch.bmm(anchors.view(b, 1, n), neighbors.view(b, n, 1)).squeeze()
        ones = torch.ones_like(similarity)
        consistency_loss = self.bce(similarity, ones)

        # Entropy loss
        entropy_loss = entropy(torch.mean(anchors, 0), input_as_probabilities = True)

        # Total loss
        total_loss = consistency_loss - self.entropy_weight * entropy_loss

        return total_loss, consistency_loss, entropy_loss

if __name__ == "__main__":
    labels = pd.read_csv("labels.csv")
    embedding_dim = 16
    dim1 = 128
    dim2 = 256

    base_model = get_resnet18(embedding_dim)
    model = BarlowModel(base_model, embedding_dim, dim1, dim2)
    model_path = "barlow_model.pt"
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()

    dataset = WhaleDataset(labels, num_samples=1, train=True, nperseg_mean=2048, nperseg_std=500)
    tp = 0
    embeddings = []
    for clip, class_name in tqdm(zip(dataset.clips, dataset.class_labels), total=len(dataset.clips)):
        image = get_random_spectrogram(clip, dataset.samplerate, nperseg_mean=2048, nperseg_std=0, shape=dataset.shape, add_noise=False)
        with torch.no_grad():
            pred = model.embed(torch.tensor(image[None, None] / image.max()))
        embeddings.append(pred.numpy()[0])

    X_in = np.stack(embeddings, axis=0)

    tree = KDTree(X_in)
    neighbour_indices = tree.query(X_in, k=2, return_distance=False)

    num_classes = len(classes)
    entropy_weight = 0.5
    learning_rate = 1e-3

    loss_fn = SCANLoss(entropy_weight=entropy_weight)
    classifier = torch.nn.Sequential(
        torch.nn.Linear(in_features=embedding_dim, out_features=32),
        torch.nn.ReLU(),
        torch.nn.Linear(in_features=32, out_features=64),
        torch.nn.ReLU(),
        torch.nn.Linear(in_features=64, out_features=num_classes),
        torch.nn.Softmax(),
    )
    optimizer = torch.optim.Adam(classifier.parameters(), lr=learning_rate)
    anchors = torch.tensor(X_in)
    neighbours = torch.tensor(X_in[neighbour_indices[:, 1]])
    num_iter = 10000
    pbar = tqdm(range(num_iter))
    losses = []
    for i in pbar:
        pred_anchors = classifier(anchors)
        pred_neighbours = classifier(neighbours)
        loss, _, _ = loss_fn(pred_anchors, pred_neighbours)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        loss = loss.item()
        losses.append(loss)
        pbar.set_description(f"loss: {loss:>7f}")

    plt.plot(losses)
    plt.show()

    final_pred = pred_anchors.detach().numpy()
    pca = PCA(n_components=2)
    transformed = pca.fit_transform(X_in)


    indices = np.argsort(dataset.class_labels)
    class_labels = np.array(dataset.class_labels)[indices]
    final_pred = final_pred[indices]
    transformed = transformed[indices]

    groups = np.split(transformed, np.unique(class_labels, return_index=True)[1][1:])

    plt.subplot(211)
    for i, group in enumerate(groups):
      plt.scatter(group[:, 0], group[:, 1], label=sorted(classes)[i])
    plt.legend()
    plt.subplot(212)
    plt.scatter(transformed[:, 0], transformed[:, 1], c=np.argmax(final_pred, axis=1))
    plt.show()

    encoder = OneHotEncoder()
    encoded = encoder.fit_transform(class_labels.reshape((-1, 1)))

    accuracies = {}
    for perm in permutations(range(num_classes)):
        classes_permuted = [classes[i] for i in perm]
        GT = torch.tensor([classes_permuted.index(x) for x in class_labels])
        PRED = torch.argmax(torch.tensor(final_pred), axis=1)
        confusion_matrix = ConfusionMatrix(classes_permuted)
        confusion_matrix.update(PRED, GT)
        accuracies[tuple(perm)] = confusion_matrix.accuracy()

    best_perm = max(accuracies, key=accuracies.get)
    classes_permuted = [classes[i] for i in best_perm]
    GT = torch.tensor([classes_permuted.index(x) for x in class_labels])
    PRED = torch.argmax(torch.tensor(final_pred), axis=1)
    c_GT = {classes_permuted[k]: v for k, v in Counter(GT.numpy()).items()}
    c_PRED = {classes_permuted[k]: v for k, v in Counter(PRED.numpy()).items()}
    confusion_matrix = ConfusionMatrix(classes_permuted)
    confusion_matrix.update(PRED, GT)
    confusion_matrix.plot()
