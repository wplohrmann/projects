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
with open("day25.txt") as f:
    lines = fmap(int, f.readlines())

def transform(n, loop_size):
    val = 1
    for _ in range(loop_size):
        val = (val * n) % 20201227
    return val
def gen_transform(n):
    val = 1
    i = 1
    while True:
        val = (val * n) % 20201227
        yield val, i
        i += 1

i = 1
i_s = []
keys = []
for key, i in gen_transform(7):
    if key in lines:
        i_s.append(i)
        keys.append(key)
        print("Added", i)
    if len(i_s) == 2:
        break
    i += 1
print(transform(keys[0], i_s[1]), "equals", transform(keys[1], i_s[0]))
