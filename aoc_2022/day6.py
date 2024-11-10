with open("day6.txt") as f:
    lines = f.read().splitlines()

line = lines[0]
for i in range(len(line)):
    s = set(line[i:i+14])
    if len(s) == 14:
        print(i + 14)
        break
