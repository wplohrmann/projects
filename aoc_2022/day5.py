import re
from collections import defaultdict

with open("day5.txt") as f:
    lines = f.read().splitlines()

stacks = defaultdict(list)
for line in lines:
    for m in re.finditer("\[(.)", line):
        stacks[m.start() // 4].append(m.group(1))
    if line.startswith("move"):
        break

stacks = [stacks[k] for k in sorted(stacks.keys())]

for line in lines:
    if line.startswith("move"):
        amount, _from, _to = re.match("move (\d+) from (\d+) to (\d+)", line).groups()
        amount, _from, _to = int(amount), int(_from), int(_to)
        stacks[_to - 1] = stacks[_from - 1][:amount][::-1] + stacks[_to - 1]
        stacks[_from - 1] = stacks[_from - 1][amount:]

print("".join([x[0] for x in stacks]))


stacks = defaultdict(list)
for line in lines:
    for m in re.finditer("\[(.)", line):
        stacks[m.start() // 4].append(m.group(1))
    if line.startswith("move"):
        break

stacks = [stacks[k] for k in sorted(stacks.keys())]

for line in lines:
    if line.startswith("move"):
        amount, _from, _to = re.match("move (\d+) from (\d+) to (\d+)", line).groups()
        amount, _from, _to = int(amount), int(_from), int(_to)
        stacks[_to - 1] = stacks[_from - 1][:amount] + stacks[_to - 1]
        stacks[_from - 1] = stacks[_from - 1][amount:]

print("".join([x[0] for x in stacks]))
