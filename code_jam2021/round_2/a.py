import numpy as np

def debug(*args, **kwargs):
    pass
debug = print

def solve():
    """
    """
    pass

if __name__=="__main__":
    T, N = map(int, input().split())

    for t in range(T):
        solution = solve()
        print("Case #"+str(t+1)+":", solution)
