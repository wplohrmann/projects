def solve(r, s):
    """
    >>> solve(2,2)
    [(2, 1)]
    >>> solve(3,2)
    [(3, 2), (2, 1)]
    """
    sequence = sum((list(range(1,r+1)) for _ in range(s)), [])
    ops = []
    sorted_sequence = sorted(sequence)
    s_ = s
    r_ = r
    while True:
        n1 = (1+s-s_)*r_
        n2 = r_-1
        ops.append((n1, n2))
        sequence[:n1+n2] = sequence[n1:n1+n2] + sequence[:n1]
        s_ -= 1
        if s_ == 1:
            r_ -= 1
            s_ = s
        if sorted_sequence == sequence:
            break



    return ops

if __name__=="__main__":
    T = int(input())

    for t in range(T):
        r, s = map(int, input().split())
        solution = solve(r, s)
        print("Case #"+str(t+1)+":", len(solution))
        for op in solution:
            print(" ".join(map(str, op)))
