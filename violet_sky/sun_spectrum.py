import numpy as np
import matplotlib.pyplot as plt

t = 5.7e3
h = 6.626e-34
k = 1.38e-23
c = 3e8

lamda = np.geomspace(10, 10000, 1000) * 1e-9
f = c / lamda

y = f**3 / (np.exp(h * f / (k * t)) - 1)
y /= np.nanmax(y)

black = "#1e1e1e"
white = "#dbdbdb"
plt.rcParams['figure.facecolor'] = black # Background color
plt.rcParams['axes.facecolor'] = black # Axes background color
plt.rcParams['text.color'] = white        # Text color
plt.rcParams['axes.labelcolor'] = white   # Axes label color
plt.rcParams['xtick.color'] = white       # X-axis tick color
plt.rcParams['ytick.color'] = white       # Y-axis tick color
plt.plot(lamda * 1e9, y, color=white)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Normalised power density")
plt.title("Power spectrum of the sun")
plt.show()
