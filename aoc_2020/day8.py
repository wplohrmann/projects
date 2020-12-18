with open("day8.txt") as f:
    lines = f.readlines()

print("Number of lines:", len(lines))
for j in range(len(lines)):
    if lines[j].startswith("jmp"):
        lines[j] = lines[j].replace("jmp", "nop")
    elif lines[j].startswith("nop"):
        lines[j] = lines[j].replace("nop", "jmp")
    else:
        continue
    acc = 0
    i = 0
    visited = set()
    while True:
        visited.add(i)
        command, amount = lines[i].split(" ")
        if command == "nop":
            i += 1
        elif command == "acc":
            acc += int(amount.strip("\n"))
            i += 1
        elif command == "jmp":
            i += int(amount.strip("\n"))
        if i in visited:
            print(i, "already visited")
            print(acc)
            break
        if i == len(lines)-1:
            print("Last instruction, acc:", acc)
            print("Line", j, "changed")
            break

    if lines[j].startswith("jmp"):
        lines[j] = lines[j].replace("jmp", "nop")
    elif lines[j].startswith("nop"):
        lines[j] = lines[j].replace("nop", "jmp")
