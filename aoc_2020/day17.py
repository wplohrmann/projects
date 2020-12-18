import re
import numpy as np
from scipy.ndimage import convolve
with open("day17.txt") as f:
    lines  = f.readlines()

with open("day17.txt") as f:
    plane = np.array(re.findall("#|\.", f.read()))

n = round(len(plane)**(1/2))
plane = np.reshape(1*(plane=="#"), ((n,n)))
if False: # part 1
    cube = np.zeros((n,n,n))
    cube[:,:,0] = plane

    kernel = np.ones((3,3,3))
    kernel[1,1,1] = 0
else: # part 2
    cube = np.zeros((n,n,n,n))
    cube[:,:,0,0] = plane

    kernel = np.ones((3,3,3,3))
    kernel[1,1,1,1] = 0

for _ in range(6):
    cube = np.pad(cube, 1)
    neighbours = convolve(cube, kernel, mode="constant")
    active_mask = (1-cube) * (neighbours==3)
    inactive_mask = cube * (1-np.isin(neighbours, [2,3]))
    cube[active_mask==1] = 1
    cube[inactive_mask==1] = 0

print(np.sum(cube))
