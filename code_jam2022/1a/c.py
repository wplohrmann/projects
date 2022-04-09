import numpy as np

def solve(es):
    """
    Find shared set for all exercises. Then cost is sum(shared) * 2 + solve(es - shared)
    If shared is empty, split exercises in half. How to split?
    """
    es = es.copy()
    if len(es) == 1:
        return np.sum(es) * 2

    shared = np.min(es, axis=0, keepdims=True)
    extra_cost = np.sum(shared) * 2
    if extra_cost > 0:
        es -= shared

    return extra_cost + min([solve(es[:i])+solve(es[i:]) for i in range(1, len(es))])

T = int(input())
for t in range(T):
    e, w = map(int, input().split())
    es = []
    for _ in range(e):
        es.append(list(map(int, input().split())))
    print(f"Case #{t+1}:", solve(np.array(es)))
