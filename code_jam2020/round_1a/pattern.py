def split(p):
    if "*" not in p:
        return p, "", ""
    first, *middle, end = p.split("*")
    return first, "*".join(middle), end

def solve(patterns):
    """
    >>> solve(["*CONUTS", "*COCONUTS"])
    'COCONUTS'
    >>> solve(["*XZ", "*XYZ"])
    '*'
    >>> solve(["COCON*", "COCONUTS*"])
    'COCONUTS'
    >>> solve(["COCON*", "*NUTS", "*CONUTS"])
    'COCONCONUTS'
    >>> solve(["H*O", "HELLO*", "*HELLO", "H*L*O"])
    'HELLOLHELLO'
    """
    longest_suffix = sorted(map(lambda p: split(p)[2], patterns), key=lambda s: -len(s))[0]
    for p in patterns:
        suffix = split(p)[2]
        if not longest_suffix.endswith(suffix):
            return "*"

    longest_prefix = sorted(map(lambda p: split(p)[0], patterns), key=lambda s: -len(s))[0]
    for p in patterns:
        prefix = split(p)[0]
        if not longest_prefix.startswith(prefix): # COCONUTS.startswith(COCON)
            return "*"

    middles = list(map(lambda p: split(p)[1], patterns))
    if not all(m=="" for m in middles):
        sub_solve = solve(middles)
        if sub_solve == "*":
            return "*"
        else:
            return longest_prefix + sub_solve + longest_suffix

    return longest_prefix+longest_suffix

if __name__=="__main__":
    T = int(input())

    for t in range(T):
        N = int(input())
        ps = []
        for n in range(N):
            ps.append(input())
        solution = solve(ps)
        print("Case #"+str(t+1)+":", solution)
