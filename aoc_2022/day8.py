import numpy as np

with open("day8.txt") as f:
    lines = f.read().splitlines()

grid = np.array([list(x) for x in lines]).astype(int)
score = 0
for i in range(1, grid.shape[0]-1):
    for j in range(1, grid.shape[1]-1):
        val = grid[i, j]
        if val > grid[i+1:, j].max() or val > grid[:i, j].max() or val > grid[i, :j].max() or val > grid[i, j+1:].max():
            score += 1

score += (grid.shape[0] + grid.shape[1] - 2) * 2
print(score)

viewing_score = np.zeros(grid.shape)
for i in range(1, grid.shape[0]-1):
    for j in range(1, grid.shape[1]-1):
        val = grid[i, j]
        east = list(grid[i+1:, j])
        above_eq = grid >= val
        break
