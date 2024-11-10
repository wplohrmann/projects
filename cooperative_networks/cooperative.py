import numpy as np
import torch
from sklearn.datasets import load_diabetes
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import trange

class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.hidden_units = [10, 100, 100, 100, 1]
        layers = []
        for i in range(len(self.hidden_units) - 1):
            layers.append(torch.nn.Linear(self.hidden_units[i], self.hidden_units[i + 1]))
            if i != len(self.hidden_units) - 2:
                layers.append(torch.nn.ReLU())

        self.fc = torch.nn.Sequential(*layers)

    def forward(self, x):
        return self.fc(x)

def loss_func(mean, log_var, y):
    assert mean.shape == log_var.shape == y.shape
    return torch.mean(torch.square(mean - y) / torch.exp(log_var) / 2 + log_var / 2)


if __name__ == "__main__":
    X, y = load_diabetes(return_X_y=True)
    for i in range(X.shape[1]):
        plt.scatter(X[:, i], y)
        plt.title(f"Feature {i}")
        plt.show()

    X = torch.tensor(X, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.float32).reshape(-1, 1)
    X_mean, X_std = X.mean(dim=0), X.std(dim=0)
    y_mean, y_std = y.mean(), y.std()
    X = (X - X_mean) / X_std
    y = (y - y_mean) / y_std

    # Predict the mean
    mean_model = Model()
    # Predict the log variance
    var_model = Model()

    mean_optimizer = torch.optim.Adam(mean_model.parameters(), lr=1e-3)
    var_optimizer = torch.optim.Adam(var_model.parameters(), lr=1e-3)

    mean_indices = torch.randperm(X.shape[0])[:X.shape[0] // 2]
    var_indices = torch.tensor([i for i in range(X.shape[0]) if i not in mean_indices])

    pbar = trange(100000)
    mean_losses = []
    var_losses = []
    for epoch in pbar:
        mean_optimizer.zero_grad()
        var_optimizer.zero_grad()

        # Mean model training
        mean_predictions = mean_model(X[mean_indices])
        with torch.no_grad():
            var_predictions = var_model(X[mean_indices])
        mean_loss = loss_func(mean_predictions, var_predictions, y[mean_indices])
        for param in mean_model.parameters():
            mean_loss += 0.01 * torch.sum(torch.square(param))
        mean_loss.backward()
        mean_optimizer.step()

        # Variance model training
        var_predictions = var_model(X[var_indices])
        with torch.no_grad():
            mean_predictions = mean_model(X[var_indices])
        var_loss = loss_func(mean_predictions, var_predictions, y[var_indices])
        for param in var_model.parameters():
            var_loss += 0.01 * torch.sum(torch.square(param))
        var_loss.backward()
        var_optimizer.step()

        if epoch % 100 == 0:
            pbar.set_description(f"Mean Loss: {mean_loss.item()}, Variance Loss: {var_loss.item()}")
        mean_losses.append(mean_loss.item())
        var_losses.append(var_loss.item())

plt.plot(mean_losses, label="Mean")
plt.plot(var_losses, label="Var")
plt.legend()
plt.show()

# Plot the predictions with uncertainty
mean_predictions = mean_model(X).detach().numpy()[:, 0]
var_predictions = np.exp(var_model(X).detach().numpy())
std_predictions = np.sqrt(var_predictions)[:, 0]
plt.errorbar(y[:, 0], mean_predictions, yerr=std_predictions, fmt='o')
plt.xlabel("True")
plt.ylabel("Predicted")
plt.show()

mse_validation = np.mean(np.square(mean_predictions[var_indices] - y[var_indices, 0].numpy()))
