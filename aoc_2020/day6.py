with open("day6.txt") as f:
    lines = f.readlines()

part_two = True

count = 0
qs = set()
first_line = True
for i, line in enumerate(lines):
    line = line.strip("\n")
    if line == "" or i == len(lines)-1:
        count += len(qs)
        qs = set()
        first_line = True
        continue
    for c in line:
        if part_two:
            if first_line:
                qs.add(c)
        else:
            qs.add(c)
    for q in qs.copy():
        if q not in line:
            qs.remove(q)
    first_line = False

print(count)

