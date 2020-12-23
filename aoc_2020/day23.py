import re
from copy import copy
from scipy.signal import convolve
import numpy as np
from itertools import product
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
from io_utils import from_grid, to_grid

with open("day23.txt") as f:
    cups = list(map(int, list(f.read().strip())))

def print_cups():
    for j, c in enumerate(cups):
        if j == current:
            print(f"({c})", end=" ")
        else:
            print(c, end=" ")
    print()

current = 0
for i in range(100):
    print("MOve", i)
    print_cups()
    cups = list(np.roll(cups, -current))
    current_value  = cups[0]
    picked_up = cups[1:4]
    print("Picked up:", picked_up)
    rest = cups[:1] + cups[4:]
    destination = rest[0]-1
    while True:
        if destination not in rest:
            destination -= 1
            if destination < min(rest):
                destination = max(rest)
            continue
        index = rest.index(destination)
        print(destination)
        break
    a = len(cups)
    cups = rest[:index+1] + picked_up + rest[index+1:]
    if len(cups) != a:
        import pdb; pdb.set_trace()
    current = (cups.index(current_value)+1) % len(cups)

current = cups.index(1)
cups = cups[current+1:] + cups[:current]
print("".join(map(str, cups)))
