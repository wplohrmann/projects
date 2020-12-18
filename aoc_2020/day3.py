from functools import reduce
with open("day3.txt") as f:
    lines = f.readlines()

cs = []
for slope in [1, 3, 5, 7, 0.5]:
    c = 0
    for i, line in enumerate(lines):
        if slope == 0.5 and i % 2 == 1:
            continue
        line = line[:-1]
        if line[int(i * slope) % len(line)] == "#":
            c += 1
    cs.append(c)
print(reduce(lambda x, y: x*y, cs))
