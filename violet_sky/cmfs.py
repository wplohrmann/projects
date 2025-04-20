from matplotlib import pyplot as plt
from sympy import symbols, Matrix, solve
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

black = "#1e1e1e"
white = "#dbdbdb"
plt.rcParams["figure.facecolor"] = black  # Background color
plt.rcParams["axes.facecolor"] = black  # Axes background color
plt.rcParams["text.color"] = white  # Text color
plt.rcParams["axes.labelcolor"] = white  # Axes label color
plt.rcParams["xtick.color"] = white  # X-axis tick color
plt.rcParams["ytick.color"] = white  # Y-axis tick color

# df = pd.read_csv("ciexyz31.csv", header=None)
df = pd.read_csv("lin2012xyz2e_1_7sf.csv", header=None)
df.columns = ["wavelength", "X", "Y", "Z"]

interp_funcs = {col: interp1d(df["wavelength"], df[col], kind='linear') for col in ["X", "Y", "Z"]}
wavelengths = np.arange(df["wavelength"].min(), df["wavelength"].max() + 1)
df = pd.DataFrame({
    "wavelength": wavelengths,
    "X": interp_funcs["X"](wavelengths),
    "Y": interp_funcs["Y"](wavelengths),
    "Z": interp_funcs["Z"](wavelengths),
})

for coord in ["X", "Y", "Z"]:
    plt.plot(df["wavelength"], df[coord], label=coord)

plt.xlabel("Wavelength (nm)")
plt.ylabel("Colour matching function")
plt.legend()
plt.show()

def with_z(arr: np.ndarray) -> np.ndarray:
    return np.concatenate([arr, 1 - arr.sum(axis=-1, keepdims=True)], axis=-1)

# sRGB basis
basis = with_z(np.array([
    [0.64, 0.33],
    [0.3, 0.6],
    [0.15, 0.06],
]))

# Display P3 basis
# basis = with_z(np.array([
#     [0.68, 0.32],
#     [0.265, 0.69],
#     [0.15, 0.06],
# ]))

# 6504 K
whitepoint_d_65 = with_z(np.array([[0.3127, 0.329]]))
# Scale to Y = 1
whitepoint_d_65 /= whitepoint_d_65[0, 1]

# Define symbols
k1, k2, k3 = symbols('k1 k2 k3')
T = Matrix(3, 3, symbols('t11 t12 t13 t21 t22 t23 t31 t32 t33'))

# Define equations
eq1 = Matrix([k1, 0, 0]) - T @ Matrix(basis[0])
eq2 = Matrix([0, k2, 0]) - T @ Matrix(basis[1])
eq3 = Matrix([0, 0, k3]) - T @ Matrix(basis[2])
eq4 = Matrix([1, 1, 1]) - T @ Matrix(whitepoint_d_65[0])

# Solve equations
solutions = solve([*eq1, *eq2, *eq3, *eq4], [k1, k2, k3] + [t for t in T])

exact_t = np.array([solutions[t] for t in T], dtype=np.float64).reshape(3, 3)

# Same as given in https://en.wikipedia.org/wiki/SRGB#Transformation
assert np.isclose(exact_t, np.array([
    [3.240625, -1.537207, -0.498628],
    [-0.969243, 1.875885, 0.041555],
    [0.055630, -0.203996, 1.057221]
]), atol=1e-3).all()



xyz = df[["X", "Y", "Z"]].values

rgb = (exact_t @ xyz.T).T
rgb_same = np.zeros_like(rgb)
for i in range(rgb.shape[0]):
    rgb_same[i] = exact_t @ xyz[i]
assert np.allclose(rgb, rgb_same)


rgb /= rgb.max()

plt.plot(df["wavelength"], rgb[:, 0], label="R", c="r")
plt.plot(df["wavelength"], rgb[:, 1], label="G", c="g")
plt.plot(df["wavelength"], rgb[:, 2], label="B", c="b")
plt.legend()
plt.xlabel("Wavelength (nm)")
plt.show()

rgb_1 = rgb.copy()
rgb_2 = rgb.copy()

# Method 1
below_0 = np.any(rgb_1 < 0, axis=-1)
rgb_1[below_0] -= np.min(rgb_1[below_0], axis=-1, keepdims=True)

# Method 2
if np.any(rgb_2 < 0):
    rgb_2 -= np.min(rgb_2)

rgb_1 /= np.max(rgb_1)
rgb_2 /= np.max(rgb_2)

# Both methods
for rgb_plot, title in zip([rgb_1, rgb_2], ["Method 1", "Method 2"]):
    corrected = np.where(rgb_plot <= 0.0031308, 12.92 * rgb_plot, 1.055 * np.power(rgb_plot, 1/2.4) - 0.055)

    plt.plot(df["wavelength"], corrected[:, 0], label="R", c="r")
    plt.plot(df["wavelength"], corrected[:, 1], label="G", c="g")
    plt.plot(df["wavelength"], corrected[:, 2], label="B", c="b")
    plt.legend()
    plt.title(title)
    plt.show()

    plt.imshow(corrected[None], extent=[df["wavelength"].min(), df["wavelength"].max(), 0, 50])
    # plt.xlim([df["wavelength"].min(), 700])
    plt.xlabel("Wavelength (nm)")
    plt.yticks([])
    plt.title(title)
    plt.show()


normalised_xyz = xyz / xyz.sum(axis=-1, keepdims=True)
assert rgb_1.max() <= 1
assert rgb_2.max() <= 1
assert rgb_1.min() >= 0
assert rgb_2.min() >= 0
xyz_1 = (np.linalg.inv(exact_t) @ rgb_1.T).T
xyz_1 /= xyz_1.sum(axis=-1, keepdims=True)
xyz_2 = (np.linalg.inv(exact_t) @ rgb_2.T).T
xyz_2 /= xyz_2.sum(axis=-1, keepdims=True)

plt.plot(normalised_xyz[:, 0], normalised_xyz[:, 1], label="Original XYZ")
plt.plot(xyz_1[:, 0], xyz_1[:, 1], label="Method 1")
plt.plot(xyz_2[:, 0], xyz_2[:, 1], label="Method 2")

plt.title("Gamut clipping")
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.show()
