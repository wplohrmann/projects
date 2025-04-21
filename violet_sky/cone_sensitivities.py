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

primaries = np.array([
    [770.49, 70.13, 0.06174579],
    [536.63, 33.61, 0.01118286],
    [430.63, 37.56, 0.01101181],
])

spectrum_r = primaries[0, 2] * np.exp(-0.5 * ((df["wavelength"] - primaries[0, 0]) / primaries[0, 1]) ** 2)
spectrum_g = primaries[1, 2] * np.exp(-0.5 * ((df["wavelength"] - primaries[1, 0]) / primaries[1, 1]) ** 2)
spectrum_b = primaries[2, 2] * np.exp(-0.5 * ((df["wavelength"] - primaries[2, 0]) / primaries[2, 1]) ** 2)

plt.plot(df["wavelength"], spectrum_r, label="Red", c="r")
plt.plot(df["wavelength"], spectrum_g, label="Green", c="g")
plt.plot(df["wavelength"], spectrum_b, label="Blue", c="b")
plt.show()

a = np.array([
    [np.sum(df[cone].values * spectrum) for cone in cones]
    for spectrum in [spectrum_r, spectrum_g, spectrum_b]
])
inv = np.linalg.inv(a.T)

rgb = (inv @ df[["Long", "Medium", "Short"]].values.T).T
rgb /= rgb.max()

plt.plot(df["wavelength"], rgb[:, 0], c="r", label="R")
plt.plot(df["wavelength"], rgb[:, 1], c="g", label="G")
plt.plot(df["wavelength"], rgb[:, 2], c="b", label="B")
plt.legend()
plt.xlabel("Wavelength (nm)")
plt.show()

