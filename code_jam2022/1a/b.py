import sys

def get_ns(n):
    ns = set()
    for i in range(30):
        ns.add(2**(29-i))
    i = 1
    others = set()
    while len(ns)+len(others) < n-1:
        if i not in ns:
            others.add(i)
        i += 1
    others.add(sum(others))
    return sorted(ns, reverse=True), sorted(others)

def solve(n):
    ns, others = get_ns(n)
    print(*ns, *others)
    judge_ns = map(int, input().split())
    judge_ns = sorted(judge_ns, reverse=True)
    a = []
    a_sum = 0
    b_sum = 0
    for ls in [judge_ns, ns]:
        for n in ls:
            if a_sum < b_sum:
                a.append(n)
                a_sum += n
            else:
                b_sum += n
    a.extend(others[:-1])
    print(*a)


T = int(input())
for t in range(T):
    n = int(input())
    solve(n)
