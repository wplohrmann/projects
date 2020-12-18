import numpy as np
import re
with open("day16.txt") as f:
    lines = f.readlines()

ranges = {}
i = 0
while True:
    line = lines[i]
    if line == "\n":
        break

    pattern = r"(.*): (\d+)-(\d+) or (\d+)-(\d+)"
    match = re.match(pattern, line)
    field, a_min, a_max, b_min, b_max = match.groups()
    a_min = int(a_min)
    a_max = int(a_max)
    b_min = int(b_min)
    b_max = int(b_max)
    ranges[field] = list(range(a_min, a_max+1)) + list(list(range(b_min, b_max+1)))
    i += 1

all_valids = set()
for field in ranges:
    all_valids.update(set(ranges[field]))
i += 2
mine = lines[i].split(",")

i += 3
others = np.loadtxt("day16.txt", skiprows=i, delimiter=",")

c=0
valid = np.ones(len(others), dtype=bool)
for i, ticket in enumerate(others):
    for el in ticket:
        if el not in all_valids:
            c += el
            valid[i] = False

print(int(c))

valid_tickets = others[valid]
possibilities = {}
for field in ranges:
    possibilities[field] = set(range(len(mine)))

for ticket in valid_tickets:
    for i, el in enumerate(ticket):
        for field in ranges:
            if el not in ranges[field]:
                try:
                    possibilities[field].remove(i)
                except KeyError:
                    pass
mapping = {}

while True:
    changed = False
    for field in possibilities:
        if len(possibilities[field]) == 1:
            i = possibilities[field].pop()
            mapping[field] = i
            changed = True
            for field in possibilities:
                try:
                    possibilities[field].remove(i)
                except KeyError:
                    pass
    if changed == False:
        break
p = 1
for field in mapping:
    if field.startswith("departure"):
        p *= int(mine[mapping[field]])

print(p)
