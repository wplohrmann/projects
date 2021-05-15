import numpy as np
from functools import reduce, lru_cache

def debug(*args, **kwargs):
    pass
# debug = print

@lru_cache(maxsize=None)
def solve(n):
    """
    >>> solve(33+48+48*13)
    7
    >>> solve(6)
    1
    >>> solve(1024)
    """
    original_n = n
    if n < 3:
        return 0

    possibilities =[]
    for factor in factors(n):
        if factor == 1:
            continue
        remainder = n//factor - 1
        possibilities.append(solve(remainder))
    return 1 + max(possibilities)


def factors(n):
    """
    >>> factors(10)
    {1, 10, 2, 5}
    >>> factors(33)
    {11, 1, 3, 33}
    """
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

if __name__=="__main__":
    T = int(input())

    for t in range(T):
        N = int(input())
        solution = solve(N)
        print("Case #"+str(t+1)+":", solution)
