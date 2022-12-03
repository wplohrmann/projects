elves = []
elf = []
while True:
    try:
        line = input()
    except EOFError:
        break
    if not line.strip():
        elves.append(elf)
        print(elf)
        elf = []
    else:
        elf.append(int(line))
elves.append(elf)

sums = sorted([sum(x) for x in elves])
print(max(sums))
print(sum(sums[-3:]))
