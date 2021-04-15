from collections import defaultdict
def solve(primes):
    """
    primes [prime] -> number in deck
    Max possible solution is max_sum
    Min possible solution is 
    """
    all_primes = sorted(list(primes.keys()))
    max_sum = sum(p*n for p,n in primes.items())
    max_sol = 0
    for i in range(max(1, max_sum-29940), max_sum):
        factors, prod = factorise(i, primes, all_primes)
        if factors is None:
            continue
        s = max_sum - sum(p*n for p,n in factors.items())
        if s==prod and s>max_sol:
            max_sol = s

    return max_sol

# all_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499]

def factorise(n, primes, all_primes):
    i = 0
    factors = defaultdict(int)
    prod = 1
    while i < len(all_primes):
        p = all_primes[i]
        n_, r = divmod(n, p)
        if r == 0:
            factors[p] += 1
            prod *= p
            n = n_
        else:
            if factors[p] > primes.get(p, 0):
                return None, None
            i += 1

    return factors, prod

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

