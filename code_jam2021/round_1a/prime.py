from itertools import product
from functools import reduce
from copy import deepcopy

def solve(primes):
    """
    primes [prime] -> number in deck
    """
    get_sum = lambda hand: sum(p*n for p,n in hand.items())
    get_prod = lambda hand: reduce(lambda x, y: x*y, (p**n for p,n in hand.items()), 1)
    assert get_sum({1: 3, 2: 5}) == 13
    assert get_prod({1: 3, 2: 5, 3: 1}) == 2**5 * 3
    # All cards in sum-hand: sum too high, so reduce it gradually. If at any point we go below that's a zero.
    # Want to get the biggest product hand.
    # print("Solving:", primes)
    max_sol = 0
    for possible_ns in product(*[range(0, n+1) for n in primes.values()]):
        # print(possible_ns)
        sum_hand = {p: possible_ns[i] for i, p in enumerate(primes.keys())}
        prod_hand = {p: primes[p] - possible_ns[i] for i, p in enumerate(primes.keys())}
        sum_n = get_sum(sum_hand)
        prod_n = get_prod(prod_hand)
        if sum_n == prod_n:
            # print("Solution:", sum_hand, prod_hand)
            if sum_n > max_sol:
                max_sol = sum_n
    return max_sol

# solve({2: 2, 3:1, 5:2, 7:1, 11:1})
# assert False

T = int(input())
for t in range(T):
    M = int(input())
    primes = {}
    for m in range(M):
        p, n = map(int, input().split())
        primes[p] = n
    solution = solve(primes)
    print("Case #"+str(t+1)+":", solution)

