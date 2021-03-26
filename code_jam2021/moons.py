import numpy as np

def _print(*args):
    # print(*args)
    pass

def possibilities(s):
    ss = [""]
    for c in s:
        if c == "?":
            ss = [substring+"C" for substring in ss] +\
                 [substring+"J" for substring in ss]
        elif c in ["C", "J"]:
            ss = [substring+c for substring in ss]
        else:
            raise ValueError("Oh no:", c)
    return ss

assert possibilities("CJ?") == ["CJC", "CJJ"]
assert set(possibilities("C?J?")) == {"CJJJ", "CJJC", "CCJC", "CCJJ"}

def get_cost(x, y, s):
    cost = 0
    last = ""
    for c in s:
        if c == "C" and last == "J":
            cost += y
        elif c == "J" and last == "C":
            cost += x
        last = c
    return cost

assert get_cost(1, 2, "CJ") == 1
assert get_cost(1, 2, "CC") == 0

def solve_naive(x, y, s):
    min_cost = 1e100
    best = None
    # for possibility in possibilities(s):
    for possibility in (s.replace("?", "C"), s.replace("?", "J")):
        cost = get_cost(x, y, possibility)
        if cost < min_cost:
            min_cost = cost
            best = possibility
    return min_cost, best

def group_s(s):
    groups = []
    state = s[0] == "?"
    group = ""
    for c in s:
        is_question = c == "?"
        if is_question == state:
            group += c
        else:
            groups.append(group)
            group = c
            state = is_question

    if is_question == state:
        groups.append(group)

    return groups


assert group_s("CJJ?J") == ["CJJ", "?", "J"]
assert group_s("CJJ?J??") == ["CJJ", "?", "J", "??"]


def solve(x, y, s):
    _print("Solving", s, "costs CJ:", x, "costs JC:", y)
    groups = group_s(s)
    _print("Groups:", groups)
    for i, group in enumerate(groups):
        if group[0] != "?":
            continue
        prepend = False
        append = False
        if i > 0:
            group = groups[i-1][-1] + group
            prepend = True
        if i < len(groups)-1:
            group = group + groups[i+1][0]
            append = True
        cost, best = solve_naive(x, y, group)
        _print(group, "->", best, "with cost", cost)
        if prepend:
            best = best[1:]
        if append:
            best = best[:-1]
        _print("Changing", groups[i], best)
        groups[i] = best

    solution = "".join(groups)
    cost= get_cost(x, y, solution)
    _print("Solution:", solution, "Cost:", cost)
    return cost, solution




T = int(input())

for t in range(T):
    x, y, s = input().split(" ")
    x = int(x)
    y = int(y)
    cost, best = solve(x, y, s)
    print("Case #"+str(t+1)+":", cost)
