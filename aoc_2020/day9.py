with open("day9.txt") as f:
    lines = f.readlines()

for i in range(25, len(lines)):
    n = int(lines[i])
    valid = False
    for n1 in lines[i-25:i]:
        for n2 in lines[i-25:i]:
            if int(n1)+int(n2) == n:
                valid = True
                break
        if valid:
            break
    if not valid:
        print(n, "not valid")
        invalid = n

stack = []
lines = list(map(int, lines))
for i in range(len(lines)):
    for j in range(i, len(lines)):
        if sum(lines[i:j]) == invalid:
            print("We did it!")
            print(min(lines[i:j]) + max(lines[i:j]))
            raise SystemExit
