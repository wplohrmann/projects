from collections import deque

def solve(ps):
    """
    Remove any pancake that appears in between two numbers that are both greater
    State only depends on maximum pancake so far
    """
    ps = deque(ps)
    most = 0
    count = 0
    while len(ps) > 0:
        if len(ps) == 1:
            d = ps.pop()
        elif ps[0] > ps[-1]:
            d = ps.pop()
        else:
            d = ps.popleft()
        if d >= most:
            count += 1
        most = max(d, most)

    return count

T = int(input())
for t in range(T):
    input()
    ps = list(map(int, input().split()))
    print(f"Case #{t+1}:", solve(ps))
