import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate2d
from scipy.ndimage.measurements import label

from Ferromagnet import * 

#Reset
N = 100 #Size of the ferromagnet
spins = reset(N,"random")



T = 2 #Temperature
M = 500 #Number of repetitions
H = 0 #Zero-field

energy_array = np.zeros(M,dtype='float') #Evolution of energy
net_mag = np.zeros(M,dtype='float') #Evolution of net magnetisation
for n in np.arange(M):
    a,b = getEnergy(spins,H)
    energy_array[n] = np.sum(a+b)
    net_mag[n] = np.sum(spins)
    spins = step(spins,T,H)
    
plt.plot(net_mag/N**2)
plt.xlabel('Number of steps',size=16)
plt.ylabel('Average spin state',size=16)
plt.title('Net magnetisation per lattice point over time',size=18)
plt.show()


plt.plot(energy_array)
plt.xlabel('Number of steps',size=16)
plt.ylabel('Total energy of the system',size=16)
plt.title('Evolution of total energy over time',size=18)
plt.show()