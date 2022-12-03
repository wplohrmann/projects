import string
chars = string.ascii_letters
with open("day3.txt") as f:
    lines = f.read().splitlines()

score = 0
for line in lines:
    left, right = line[:len(line) // 2], line[len(line) // 2:]
    common = set(left).intersection(set(right)).pop()
    add = chars.index(common) + 1
    score += add
print(score)


score = 0
for i in range(0, len(lines), 3):
    group = lines[i:i+3]
    common = set(group[0]).intersection(group[1]).intersection(group[2]).pop()
    add = chars.index(common) + 1
    score += add
print(score)

