import numpy as np
from scipy.signal import convolve2d
with open("day11.txt") as f:
    lines = f.readlines()

seats = np.array(list(map(lambda line: list(line.strip("\n")), lines)))
seats = seats == "L"
taken = 0
state = seats.copy()
kernel = np.array([1,1,1,1,0,1,1,1,1]).reshape((3,3))
part_one = True
while True:
    neighbours = convolve2d(state, kernel, mode="same")
    state[neighbours >= 4] = 0 # More than 4 neighbours => Empty

    state[neighbours == 0] = 1 # No neighbours => Occupied
    state *= seats # Can only sit in a seat
    new_taken = np.sum(state)
    if new_taken == taken:
        print(taken)
        break
    taken = new_taken

state = seats.copy()
taken = 0
while True:
    neighbours = np.zeros(state.shape)
    for i in range(seats.shape[0]):
        for j in range(seats.shape[1]):
            for d in [[0,1],
                      [0,-1],
                      [1,0],
                      [-1,0],
                      [1,1],
                      [-1,-1],
                      [-1,1],
                      [1,-1]]:
                for r in range(1,8):
                    try:
                        k = i+d[0]*r
                        l = j+d[1]*r
                        assert 0 <= k <= state.shape[0]-1
                        assert 0 <= l <= state.shape[1]-1
                    except AssertionError:
                        continue
                    if seats[k,l]:
                        neighbours[i,j] += state[k,l]
                        break
    state[neighbours >= 5] = 0 # More than 4 neighbours => Empty

    state[neighbours == 0] = 1 # No neighbours => Occupied
    state *= seats # Can only sit in a seat
    new_taken = np.sum(state)
    if new_taken == taken:
        print(taken)
        break
    taken = new_taken
