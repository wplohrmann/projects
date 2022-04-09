import numpy as np

def println(k, n):
    for i in range(n):
        print(k, end="")
    print(k[0])

def solve(r, c):
    for i in range(r):
        if i == 0:
            print("..", end="")
            println("+-", c-1)
            print("..", end="")
            println("|.", c-1)
        else:
            println("+-", c)
            println("|.", c)
    println("+-", c)


    print()
    return r, c, type(r)

T = int(input())
for t in range(T):
    r, c = input().split()
    print(f"Case #{t+1}:")
    solve(int(r), int(c))
