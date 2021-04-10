from math import sqrt
def solve(square):
    """
    square :: [[int]] of shape n,n
    """
    n = int(sqrt(len(square)))
    k = sum(square[i*n+i] for i in range(n))
    r = c = 0
    for i in range(n):
        if len(set(square[i*n:(i+1)*n])) != n:
            r += 1
        if len(set(square[i::n])) != n:
            c += 1
    return k, r, c

t = int(input())
for i in range(t):
    n = int(input())
    square = []
    for _ in range(n):
        line = list(map(int, input().split(" ")))
        square.extend(line)
    print("Case #"+str(i+1)+":", *solve(square))
