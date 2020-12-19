import numpy as np
import sys
import re
with open("day19.txt") as f:
    lines = f.readlines()
def join(l):
    l2 = list(map(lambda s: f"({s})" if "|" in s else s, l))
    return "".join(l2)

patterns = {}
def solve(i):
    if i in patterns:
        return patterns[i]
    line = rules[i]
    if "|" in line:
        m = re.search(": (.*)\|(.*)", line)
        part1 = m.group(1).split()
        part2 = m.group(2).split()
        patterns[i] = join(solve(int(i)) for i in part1) + "|" + join(solve(int(i)) for i in part2)
        print("Added pattern!", patterns[i])
        return patterns[i]
    elif "\"" not in line:
        if i == 8:
            patterns[i] = f"(({solve(42)})+)"
        elif i == 11:
            patterns[i] = "(" + "|".join(f"(({solve(42)}){{{k}}}({solve(31)}){{{k}}})" for k in range(1,10)) + ")"
        if False:
            pass
        else:
            m = re.search(": (.*)", line)
            part1 = m.group(1).split()
            patterns[i] = join(solve(int(i)) for i in part1)
        print("Added pattern!", patterns[i])
        return patterns[i]
    if "a" in line:
        patterns[i] = "a"
        print("Added pattern!", patterns[i])
        return "a"
    if "b" in line:
        patterns[i] = "b"
        print("Added pattern!", patterns[i])
        return "b"


rules = {}
for line in lines:
    if ":" not in line:
        break
    i = int(re.match("(\d+):", line).group(1))
    rules[i] = line

pattern = solve(0) + "$"
c = 0
for i, line in enumerate(lines):
    if ":" in line:
        continue
    m = re.match(pattern, line)
    if m is not None:
        print("Match!", line.strip())
        c += 1
    else:
        print("no match!", line.strip())
print(c)
