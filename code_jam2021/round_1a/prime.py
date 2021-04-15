def solve(primes):
    """
    primes [prime] -> number in deck
    Max possible solution is max_sum
    """
    max_sum = sum(p*n for p,n in primes.items())
    solutions = [(1,0)] # Tuples (prod,sum)
    max_sol = 0
    remaining_sum = max_sum
    for p in primes:
        for n in range(primes[p]):
            new_solutions = set()
            for sol in solutions:
                add_to_prod = (sol[0]*p, sol[1])
                add_to_sum = (sol[0], sol[1]+p)
                if add_to_prod[0] >= max_sum: # We need to add the rest of the cards to the sum instead, so can immediately get the end state
                    if sol[0] == sol[1]+remaining_sum and sol[0] > max_sol:
                        max_sol = sol[0]
                else: # Only add to possibilities if it's still possible to add to prod hand
                    new_solutions.add(add_to_sum)
                    new_solutions.add(add_to_prod)
            remaining_sum -= p

            solutions = new_solutions

    for sol in solutions:
        if sol[0] == sol[1] and sol[0] > max_sol:
            max_sol = sol[0]

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

