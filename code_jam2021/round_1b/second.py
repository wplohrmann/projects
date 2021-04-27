import numpy as np
from itertools import count


def debug(*args, **kwargs):
    pass
# debug = print

def solve(a, b, required):
    """
    """
    for i in count(len(required)):
        if can_make(i, required):
            return i
        debug("Can't make with", i)

    return None

def can_make(i, required):
    have = {i: 1}
    want = {j+1:x for j, x in enumerate(required)}
    while True:
        debug(have, want)
        for m, amount in have.copy().items():
            if m in want and want[m] > 0:
                subtracted = min(want[m], have[m])
                want[m] -= subtracted
                have[m] -= subtracted
                if have[m] == 0:
                    del have[m]
        if sum(want.values()) == 0:
            return True # We did it!
        if sum(have.values()) == 0:
            return False # There are still required items

        max_element = max(have.keys())
        if max_element-1 in have:
            have[max_element-1] += 1
        elif max_element-1 < 1:
            pass
        else:
            have[max_element-1] = 1

        if max_element-2 in have:
            have[max_element-2] += 1
        elif max_element-2 < 1:
            pass
        else:
            have[max_element-2] = 1
        if have[max_element] == 1:
            del have[max_element]
        else:
            have[max_element] -= 1

    
if __name__=="__main__":
    T = int(input())

    for t in range(T):
        N, A, B = map(int, input().split())
        required = list(map(int, input().split()))
        solution = solve(A, B, required)
        if solution is not None:
            print("Case #"+str(t+1)+":", solution)
        else:
            print("Case #"+str(t+1)+":", "IMPOSSIBLE")

