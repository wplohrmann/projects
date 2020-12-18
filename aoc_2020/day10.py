import numpy as np
with open("day10.txt") as f:
    lines = f.readlines()
lines = list(map(int, lines))

lines = np.array([0] + sorted(lines) + [max(lines)+3])
diffs = np.diff(lines)
print(np.sum(diffs==3) * np.sum(diffs==1))

ones = []
length = 0
for diff in diffs:
    if diff == 1:
        length += 1
    elif diff == 3:
        ones.append(length)
        length = 0
    else:
        raise ValueError("")

prod = 1
for one in ones:
    prod *= {0: 1, 1: 1, 2: 2, 3: 4, 4: 7}[one]
print(prod)


