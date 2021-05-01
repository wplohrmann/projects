import numpy as np

def debug(*args, **kwargs):
    pass
# debug = print
    
def solve(n):
    """
    """
    s = str(n)
    ys = []
    N1 = 100
    N2 = 100
    for i in range(1, len(s)+1):
        for k in range(-2000, 2000):
            first_n = int(s[:i])+k
            if first_n < 0:
                continue
            debug("First n:", first_n)
            next_roaring = ""
            for j in range(N2):
                next_roaring += str(first_n+j)
                if int(next_roaring) > n and j > 0:
                    debug("First n:", first_n, "NExt roaring:", next_roaring)
                    ys.append(next_roaring)
                    break
            # debug(i, first_n)

    return min(map(int, ys))
if __name__=="__main__":
    T = int(input())

    for t in range(T):
        n = int(input())
        solution = solve(n)
        print("Case #"+str(t+1)+":", solution)

