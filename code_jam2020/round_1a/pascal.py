from math import factorial
from scipy.special import binom
from functools import reduce
from itertools import count

def ncr(pos):
    """
    >>> ncr((4, 3))
    3
    >>> ncr((4, 4))
    1
    >>> ncr((14, 14))
    1
    >>> ncr((14, 13))
    13
    >>> ncr((14, 2))
    13
    >>> ncr((14, 1))
    1
    """
    n, r = pos[0]-1, pos[1]-1
    return int(binom(n, r))

def solve(n):
    """
    >>> solve(1)
    [(1, 1)]
    >>> ans = solve(4)
    >>> ans = solve(499)
    >>> ans = solve(500)
    >>> ans = solve(501)
    >>> ans = solve(502)
    >>> ans = solve(int(1e4))
    >>> ans = solve(int(1e5))
    >>> ans = solve(int(1e6))
    >>> ans = solve(int(1e7))
    >>> ans = solve(int(1e8))
    >>> ans = solve(int(1e9))
    """
    if n < 500:
        path = [(i+1, i+1) for i in range(n)]
    else:
        path = [(1, 1)]
        bin_rep = list(reversed(bin(n-30)[2::]))[1:]
        for digit in bin_rep:
            current = path[-1]
            if digit == "1":
                if current[1] == 1: # We're on the left side, so go right
                    path.extend([(current[0]+1, i) for i in range(1, current[0]+2)])
                else:
                    path.extend([(current[0]+1, i) for i in range(current[0]+1, 0, -1)])
            else:
                if current[1] == 1: # We're on the left side, so just use c=1
                    path.append((current[0]+1, 1))
                else:
                    path.append((current[0]+1, current[0]+1))

        remaining = n - sum(map(ncr, path))
        if remaining < 0 or remaining > 500 - len(path):
            import pdb; pdb.set_trace()
            print("hoops")

        current = path[-1]
        if current[1] == 1:
            path.extend([(i+current[0]+1, 1) for i in range(remaining)])
        else:
            path.extend([(i+current[0]+1, i+current[0]+1) for i in range(remaining)])


    assert len(path) <= 500
    try:
        assert sum(map(ncr, path)) == n
    except:
        import pdb; pdb.set_trace()
        print("PDB TIME")
    
    try:
        assert len(set(path)) == len(path)
    except:
        import pdb; pdb.set_trace()
        print("PDB TIME")
    

    return path

if __name__=="__main__":
    T = int(input())

    for t in range(T):
        n = int(input())
        solution = solve(n)
        print("Case #"+str(t+1)+":")
        for pos in solution:
            print(pos[0], pos[1])
