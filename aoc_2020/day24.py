import re
# from scipy.signal import convolve
from copy import copy
import matplotlib.pyplot as plt
import numpy as np
from itertools import product
from collections import defaultdict, Counter
from io_utils import from_grid, to_grid
from linked_list import Node
from prelude import join, fmap

part_two = False
with open("day24.txt") as f:
    lines = f.readlines()

tiles = []
prefix = ""
for line in lines:
    tile=  []
    for c in line.strip("\n"):
        if c in "sn":
            prefix = c
        else:
            tile.append(prefix+c)
            prefix=""
    tiles.append(tile)
coordinates = defaultdict(int)
for tile in tiles:
    i = j = 0
    for c in tile:
        if c=="e":
            j+=1
        elif c=="se":
            i+=1
        elif c=="sw":
            i+=1
            j-=1
        elif c=="w":
            j-=1
        elif c=="nw":
            i-=1
        elif c=="ne":
            i-=1
            j+=1
    coordinates[(i,j)] = 1 - coordinates[(i,j)]
print("Day 0:", sum(coordinates.values()))
def plot():
    for (i, j) in neighbours:
        x = j+i*0.5
        y = -np.sqrt(3)/2 * i
        if coordinates[(i,j)] == 1:
            plt.scatter([x], [y], c="g")
        else:
            plt.scatter([x], [y], c="r")
        plt.annotate(str(neighbours[(i,j)]) + ", " + str((i,j)), (x, y))

    plt.gca().set_aspect("equal")
    plt.show()

for day in range(1,101):
    neighbours = defaultdict(int)
    for (i,j), v in copy(coordinates).items():
        assert v in [0,1]
        if v:
            for c in [(i,j-1),(i,j+1),(i+1,j-1),(i+1,j),(i-1,j),(i-1,j+1)]:
                neighbours[c] += 1
            neighbours[(i,j)] += 0
    assert sum(neighbours.values()) == 6 * sum(coordinates.values())
    # plot()
    for c,n in neighbours.items():
        assert coordinates[c] in [1,0]
        if coordinates[c] == 1 and (n not in [1,2]):
            coordinates[c] = 0
        elif coordinates[c] == 0 and n == 2:
            coordinates[c] = 1
    # plot()

    if day < 10 or day % 10 == 0:
        print("Day", day, ":", sum(coordinates.values()))
