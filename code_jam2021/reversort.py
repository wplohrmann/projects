import numpy as np

def reverse(l):
    for i in range(len(l)//2):
        l[i], l[-i-1] = l[-i-1], l[i]
    return l

def solve(integers):
    n = len(integers)
    cost = 0
    for i in range(n-1):
        j = i+np.argmin(integers[i:])
        cost += j-i+1
        integers[i:j+1] = reverse(integers[i:j+1])
        assert len(integers) == n

    return cost

T = int(input())

for t in range(T):
    n = int(input())
    integers = list(map(int, input().split(" ")))
    print("Case #"+str(t+1)+":", solve(integers))
