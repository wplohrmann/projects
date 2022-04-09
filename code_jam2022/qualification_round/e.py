import sys
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import random

def read():
    return map(int, input().split())

def solve(n, k):
    room, num_passages = read()
    values1 = []
    values2 = []
    for i in range(k // 2):
        print("T", random.randint(1, n))
        _, num_passages = read()
        values1.append(num_passages)
        # Don't record it
        # passages[room1] = num_passages
        print("W")
        _, num_passages = read()
        values2.append(num_passages)

    values1 = np.array(values1)
    values2 = np.array(values2)
    bins = np.linspace(min(np.min(values1), np.min(values2)), max(np.max(values1), np.max(values2)))
    mids = (bins[:-1] + bins[1:]) / 2
    hist1, _ = np.histogram(values1, bins=bins)
    hist2, _ = np.histogram(values2, bins=bins)
    plt.plot(hist1 * mids, hist2, "o")
    plt.title(f"{np.mean(values1)=}, {np.mean(values2)=}")
    plt.show()
    edges = n / np.mean(1/values2) / 2

    print("E", int(edges))

T = int(input())
for t in range(T):
    n, k = map(int, input().split())
    solve(n, k)
