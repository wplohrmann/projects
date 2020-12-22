import re
from copy import copy
from scipy.signal import convolve
import numpy as np
from itertools import product
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
from io_utils import from_grid, to_grid

with open("day22.txt") as f:
    p1, p2 = f.read().split("\n\n")
    p1 = list(map(int, p1.splitlines()[1:]))
    p2 = list(map(int, p2.splitlines()[1:]))

def get_score(p):
    return sum([(i+1)*c for i, c in enumerate(p[::-1])])


while len(p1)*len(p2) > 0:
    print(p1, p2)
    if p1[0] == p2[0]:
        raise ValueError
    if p1[0] > p2[0]:
        print("Player 1 wins!")
        p1 = p1[1:] + [p1[0], p2[0]]
        p2 = p2[1:]
    elif p2[0] > p1[0]:
        print("Player 2 wins!")
        p2 = p2[1:] + [p2[0], p1[0]]
        p1 = p1[1:]

if len(p1) == 0:
    score = get_score(p2)
if len(p2) == 0:
    score = get_score(p1)

print(score)
print("New game!")

def play(p1, p2, game=1):
    r = 0
    states = set()
    while len(p1)*len(p2) > 0:
        r += 1
        state = str((p1, p2))
        if state in states:
            if game == 1:
                score= get_score(p1)
                print(score)
            return True
        states.add(state)
        print(p1, p2)
        c1 = p1.pop(0)
        c2 = p2.pop(0)
        if c1 <= len(p1) and c2 <= len(p2):
            print("Subgame!")
            p1_wins_round = play(copy(p1[:c1]), copy(p2[:c2]), game=game+1)
        else:
            p1_wins_round = c1 > c2
        if p1_wins_round:
            print(f"Player 1 wins round {r} of game {game}!")
            p1.append(c1)
            p1.append(c2)
        else:
            print(f"Player 2 wins round {r} of game {game}!")
            p2.append(c2)
            p2.append(c1)
    winner = len(p1) > len(p2)
    if winner:
        print(f"Player 1 wins game {game}")
    else:
        print(f"Player 2 wins game {game}")
    if game == 1:
        if winner:
            score = get_score(p1)
        else:
            score = get_score(p2)
        print(score)
    return winner

with open("day22.txt") as f:
    p1, p2 = f.read().split("\n\n")
    p1 = list(map(int, p1.splitlines()[1:]))
    p2 = list(map(int, p2.splitlines()[1:]))

p1_wins = play(p1, p2)
