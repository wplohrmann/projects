import numpy as np

def debug(*args, **kwargs):
    pass
# debug = print

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
            union = 0
            for offset in [-1, 0, 1]:
                best = (unique[i-1]+unique[i]) // 2 +offset
                distance_up = unique[i]-best-1 # nums in between
                distance_down = best - unique[i-1]-1 # nums in between
                upper = best+distance_up//2
                lower = best-distance_down//2
                if upper-lower+1 > union:
                    union = upper-lower+1
                    _lower = lower
                    _upper = upper
                    _best = best
            area = (_lower, _upper, _best)
        areas.append(area)
    if unique[-1]+1 <= k:
        areas.append((unique[-1]+1, k, unique[-1]+1))
    best = 0
    debug("UNique:", unique)
    debug("len(areas", len(areas), "len(unique)", len(unique))
    for i in range(len(areas)):
        for j in range(len(areas)): # i  and j are the segments where each ticket goes (1..unique[i]) 
            union = 0
            union += areas[i][1] - areas[i][0] + 1
            if i != j:
                union += areas[j][1] - areas[j][0] + 1 # Different segments

            if union > best:
                best = union
    for i in range(len(unique)):
        if i == 0:
            continue
        union = unique[i]-unique[i-1]-1
        if union > best:
            best=  union
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
