import numpy as np
from itertools import permutations

def reverse(l):
    for i in range(len(l)//2):
        l[i], l[-i-1] = l[-i-1], l[i]
    return l

def reversort(integers):
    integers = integers.copy()
    n = len(integers)
    cost = 0
    for i in range(n-1):
        j = i+np.argmin(integers[i:])
        cost += j-i+1
        integers[i:j+1] = reverse(integers[i:j+1])
        assert len(integers) == n

    return cost, integers

def get_subcosts(n, c):
    costs = list(range(2, n+1))[::-1]
    excess = sum(costs) - c
    if excess < 0:
        return None
    for i, cost in enumerate(costs):
        if excess == 0:
            return costs
        trim = min(excess, cost-1)
        excess -= trim
        costs[i] -= trim
    if excess == 0:
        return costs

    return None

def solve_naive(n, c):
    ordered = list(range(1, n+1))
    for permutation in permutations(ordered):
        permutation = list(permutation)
        cost, _ = reversort(permutation)
        if cost == c:
            return permutation

def solve(n, c):
    costs = get_subcosts(n, c)
    if costs is None:
        return None

    ordered = list(range(1, n+1))
    for i in range(n-1)[::-1]: # Do the reversort in reverse (reversereversort?)
        cost = costs[i]
        j = cost + i - 1
        ordered[i:j+1] = reverse(ordered[i:j+1])
    cost, integers = reversort(ordered)
    # print(cost, c, n, ordered)

    return ordered

T = int(input())

for t in range(T):
    n, c = input().split()
    n = int(n)
    c = int(c)
    solution = solve(n, c)
    if solution is None:
        print("Case #"+str(t+1)+":", "IMPOSSIBLE")
    else:
        print("Case #"+str(t+1)+":", *solution)
