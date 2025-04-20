import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

black = "#1e1e1e"
white = "#dbdbdb"
plt.rcParams["figure.facecolor"] = black  # Background color
plt.rcParams["axes.facecolor"] = black  # Axes background color
plt.rcParams["text.color"] = white  # Text color
plt.rcParams["axes.labelcolor"] = white  # Axes label color
plt.rcParams["xtick.color"] = white  # X-axis tick color
plt.rcParams["ytick.color"] = white  # Y-axis tick color

df = pd.read_csv("linss2_10e_1_8dp.csv", header=None)
df.fillna(0, inplace=True)
cones = ["Long", "Medium", "Short"]
df.columns = ["wavelength"] + cones
colours = ["r", "g", "b"]
for cone, c in zip(cones, colours):
    plt.plot(df["wavelength"], df[cone], label=cone, c=c)

plt.xlim([390, 700])
plt.xlabel("Wavelength (nm)")
plt.ylabel("Sensitivity")
plt.title("Cone sensitivities")
plt.legend()
plt.show()

cie_rgb_basis = np.array([650, 530, 460])
a = np.zeros((3, 3))
for j, lamda in enumerate(cie_rgb_basis):
    for i, cone in enumerate(cones):
        x = df["wavelength"].values
        y = df[cone].values
        splev = interp1d(x, y, kind="linear")
        a[i, j] = splev(lamda)

print(np.round(a, 2))

wavelengths = np.linspace(df["wavelength"].min(), df["wavelength"].max(), 1000)
excitations = np.zeros((500, len(wavelengths), 3))
for i, cone in enumerate(cones):
    x = df["wavelength"].values
    y = df[cone].values
    splev = interp1d(x, y, kind="linear")
    for j, lamda in enumerate(wavelengths):
        excitations[:, j, i] = splev(lamda)

rgbs = np.zeros(excitations.shape)
inv = np.linalg.inv(a)
for j in range(excitations.shape[1]):
    rgbs[:, j] = inv @ excitations[0, j]

below_0 = np.any(rgbs < 0, axis=2)
rgbs[below_0] -= np.min(rgbs[below_0], axis=-1, keepdims=True)
rgbs /= np.max(rgbs)
rgbs = np.where(rgbs <= 0.0031308, 12.92 * rgbs, 1.055 * np.power(rgbs, 1/2.4) - 0.055)
plt.imshow(rgbs, extent=[wavelengths[0], wavelengths[-1], 0, 50])
plt.xlabel("Wavelength (nm)")
plt.show()
