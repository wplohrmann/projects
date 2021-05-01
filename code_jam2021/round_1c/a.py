import numpy as np

def debug(*args, **kwargs):
    pass
debug = print

def solve(n, k, tickets):
    """
    """
    unique = list(sorted(set(tickets)))
    areas = []
    debug(unique)
    for i, ticket in enumerate(unique):
        # Choose best ticket in interval (1 .. ticket) or unique[i-1] .. ticket[i]
        if i == 0 and ticket > 1:
            best = ticket-1
            area = (1, ticket-1, ticket-1)
        elif i == 0:
            continue
        elif unique[i]-unique[i-1] == 1: # No chance of winning here
            continue
        elif unique[i]-unique[i-1] == 2:
            best = unique[i]-1
            area = (best, best, best)
        else:
            assert i > 0
            best = (unique[i-1]+unique[i]) // 2
            distance_up = unique[i]-best-1 # nums in between
            distance_down = best - unique[i-1]-1 # nums in between
            upper = best+distance_up//2
            lower = best-distance_down//2
            if distance_up%2 ==1 and distance_down%2 == 1:
                best -= 1
                lower -= 1
            area = (lower, upper, best)
        areas.append(area)
    if unique[-1]+1 <= k:
        areas.append((unique[-1]+1, k, unique[-1]+1))
    best = 0
    for i in range(len(areas)):
        for j in range(len(areas)):
            union = 0
            union += areas[i][1] - areas[i][0] + 1
            if i != j:
                union += areas[j][1] - areas[j][0] + 1 # Otherwise they're identical
            if union > best:
                best = union
    debug(areas)
    return best / k

if __name__=="__main__":
    T = int(input())

    for t in range(T):
        N, K = map(int, input().split())
        tickets = list(map(int, input().split()))
        solution = solve(N, K, tickets)
        if solution is not None:
            print("Case #"+str(t+1)+":", solution)
        else:
            print("Case #"+str(t+1)+":", "IMPOSSIBLE")
