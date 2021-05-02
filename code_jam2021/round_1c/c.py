import numpy as np

def debug(*args, **kwargs):
    pass
# debug = print

def double(x):
    return x + "0"

def negate(x):
    """
    >>> negate("101")
    '10'
    >>> negate("1000")
    '111'
    >>> negate("0")
    '1'
    >>> negate("1")
    '0'
    >>> negate("1111111111")
    '0'
    """
    if x == "1"*len(x):
        return "0"
    return x.translate(str.maketrans({"0": "1", "1": "0"})).lstrip("0")

def solve(start, stop):
    """
    """
    states = set()
    states.add(start)
    N = 40
    for i in range(N):
        if stop in states:
            return i
        new_states = set()
        for state in states:
            new_states.add(double(state))
            new_states.add(negate(state))
        states = new_states
        debug(len(states))
    if stop in states:
        return i+1
    else:
        debug(len(states))
        return "IMPOSSIBLE"


if __name__=="__main__":
    T = int(input())

    for t in range(T):
        start, stop = input().split()
        solution = solve(start, stop)
        print("Case #"+str(t+1)+":", solution)
