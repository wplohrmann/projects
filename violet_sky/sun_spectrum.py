import numpy as np
import matplotlib.pyplot as plt

black = "#1e1e1e"
white = "#dbdbdb"
plt.rcParams['figure.facecolor'] = black # Background color
plt.rcParams['axes.facecolor'] = black # Axes background color
plt.rcParams['text.color'] = white        # Text color
plt.rcParams['axes.labelcolor'] = white   # Axes label color
plt.rcParams['xtick.color'] = white       # X-axis tick color
plt.rcParams['ytick.color'] = white       # Y-axis tick color

t = 5772
h = 6.626e-34
k = 1.38e-23
c = 299_792_458

lamda = np.geomspace(10, 5000, 1000) * 1e-9
f = c / lamda

y = lamda**(-5) / (np.exp(h * f / (k * t)) - 1)
y /= np.nanmax(y)
peak_wavelength = lamda[np.argmax(y)] * 1e6


plt.axvline(peak_wavelength, color='red', linestyle='--', label=f'Peak: {peak_wavelength:.2f} um')
plt.legend()
plt.plot(lamda * 1e6, y, color=white)
plt.xlabel("Wavelength (um)")
plt.ylabel("Normalised power density")
plt.title("Power spectrum of the sun")
plt.show()
