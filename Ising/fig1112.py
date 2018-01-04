import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate2d

from Ferromagnet import * 

#Creates a 2d array with values equal to H_scalar, except in a circle in the 
#middle, which is now at H=100
def circle_H(H_scalar,N):
    H_grid = H_scalar*np.ones((N,N))
    x = np.linspace(-N/2,N/2,N)
    xx,yy = np.meshgrid(x,x)
    H_grid[xx**2+yy**2 < N**2/49] = 20 #Strong magnetic field in a small circle
    return H_grid
#Reset
N = 100 #Size of the ferromagnet
spins = reset(N,"random")

T = Tc*1.5

M = 125
for n in np.arange(M):
    H_grid = circle_H(0,N)
    spins = step(spins,T,H_grid)


plt.imshow(spins,interpolation='none',clim=(-1,1))
plt.axis('off')
plt.title('Lattice with a permanently magnetised region, T= 1.5 Tc',size=18)
plt.show()