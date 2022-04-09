def solve(x):
    r = []
    current = None
    for c in x:
        if current is None:
            current = c
            counter = 1
        elif c == current:
            counter += 1
        else:
            r.append((current, counter))
            counter = 1
            current = c
    r.append((current, counter))

    s = []
    for i, (c, count) in enumerate(r):
        if i == len(r) -1:
            s.extend([c for _ in range(count)])
            continue
        next_c, _ = r[i+1]
        if next_c > c:
            s.extend([c for _ in range(count*2)])
        else:
            s.extend([c for _ in range(count)])
    return "".join(s)




T = int(input())
for t in range(T):
    x = input()
    print(f"Case #{t+1}:", solve(x))
