import numpy as np

def solve(printers):
    # print(printers)
    maximum = [min([printers[i][j] for i in range(3)]) for j in range(4)]
    # print("Max", maximum)
    if sum(maximum) < 1e6:
        return ["IMPOSSIBLE"]
    answer = [maximum[0]]
    for i in range(1, 4): # Rest of the colours
        so_far = sum(answer)
        if so_far < 1e6:
            answer.append(min(maximum[i], int(1e6-so_far)))
        else:
            answer.append(0)
    return answer

T = int(input())
for t in range(T):
    printers = []
    for i in range(3):
        printers.append([int(x) for x in input().split()])
    print(f"Case #{t+1}:", *solve(printers))
