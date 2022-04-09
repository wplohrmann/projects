from collections import defaultdict

def is_perm(a, b):
    return a!=b and set(a) == set(b)

def solve(fun, conf):
    inits = set(range(len(fun))) - set(conf)
    triggers = defaultdict(set)
    for i in inits:
        to_trigger = [i]
        while len(to_trigger):
            n = to_trigger.pop()
            triggers[(i,)].add(n)
            if conf[n] != -1:
                to_trigger.append(conf[n])
    triggers = dict(triggers)

    scores = {(i,): max((fun[x] for x in triggers[(i,)])) for i in inits}
    for _ in range(len(inits)-1):
        new_scores = {}
        for key, score in scores.items():
            triggered = triggers[tuple(sorted(key))]
            for i in inits - set(key):
                new_score = score + max((fun[x] for x in triggers[(i,)] if x not in triggered))
                new_key = tuple(sorted(key + (i,)))
                existing_score = new_scores.get(new_key, 0)
                if new_score > existing_score:
                    new_scores[new_key] = new_score
                triggers[new_key] = triggers[key].union(triggers[(i,)])
        scores = new_scores


    return max(scores.values())

T = int(input())
for t in range(T):
    input()
    fun = [int(x) for x in input().split()]
    conf = [int(x)-1 for x in input().split()]
    assert len(fun) == len(conf)
    print(f"Case #{t+1}:", solve(fun, conf))
