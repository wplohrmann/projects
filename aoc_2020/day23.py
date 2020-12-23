import re
from copy import copy
from scipy.signal import convolve
import numpy as np
from itertools import product
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
from io_utils import from_grid, to_grid
from linked_list import Node
from prelude import join

with open("day23.txt") as f:
    lst = list(map(int, list(f.read().strip())))

part_two = False
if part_two: # part 2
    N = 1000000
else:
    N = 9
lst = lst + list(range(max(lst)+1, N+1))
assert len(lst) == N

lookup = {}

cup = Node(lst[0])

last = cup
lookup[last.val] = last
for c in lst[1:]:
    last.next = Node(c)
    last = last.next
    lookup[last.val] = last
last.next = cup

if part_two:
    steps = 10000000
else:
    steps = 100
for i in range(steps):
    # print(f"-- move {i} --")
    # print(f"cups: {cup.list()}")
    if i % 100000 == 0:
        print(i)
    pickup_begin = cup.next
    vals = [pickup_begin, pickup_begin.next, pickup_begin.next.next]
    destination_val = cup.val - 1
    while destination_val == 0 or lookup[destination_val] in vals:
        destination_val -= 1
        if destination_val < 1:
            destination_val = N
    destination = lookup[destination_val]
    next_after = destination.next
    destination.next = vals[0]
    cup.next = vals[-1].next
    vals[-1].next = next_after
    cup = cup.next

if not part_two:
    print(join(lookup[1].list()[1:]))
else:
    a, b = lookup[1].next, lookup[1].next.next
    print(a.val*b.val)
