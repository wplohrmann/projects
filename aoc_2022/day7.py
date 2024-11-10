import os
import re
from collections import defaultdict

with open("day7.txt") as f:
    lines = f.read().splitlines()

tree = {}
command = None
cwd = ""
for line in lines:
    if line.startswith("$ ls"):
        command = "ls"
        continue
    if line.startswith("$ cd"):
        m = re.match("\$ cd (.*)", line)
        if m.group(1) == "..":
            cwd = os.path.dirname(cwd)
        else:
            cwd = os.path.join(cwd, m.group(1))
        continue
    if command == "ls":
        if line.startswith("dir"):
            tree[os.path.join(cwd, line[len("dir "):])] = None
        else:
            tree[os.path.join(cwd, line.split(" ")[1])] = int(line.split(" ")[0])

sizes = defaultdict(int)
for dir in tree:
    if tree[dir] is not None:
        continue
    for file in tree:
        if file.startswith(dir):
            if isinstance(tree[file], int):
                sizes[dir] += tree[file]

sizes = dict(sizes)

score = 0
for size in sizes.values():
    if size < 100000:
        score += size
print(score)

outermost = sum(value for key, value in sizes.items() if key.startswith("/") and key.count("/") == 1)
for size in sorted(sizes.values()):
    free_after = 70000000 - outermost + size
    required = 30000000
    if free_after > required:
        print(size)
        break
