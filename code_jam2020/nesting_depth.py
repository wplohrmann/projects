from collections import defaultdict
def solve(s):
    integers = list(map(int, list(s)))
    nesting_level = 0
    parens = defaultdict(str)
    for i, n in enumerate(integers):
        if n > nesting_level:
            parens[i] = "(" * (n - nesting_level)
            nesting_level = n
        elif n < nesting_level:
            parens[i] = ")" * (nesting_level - n)
            nesting_level = n
    if nesting_level > 0:
        parens[i+1] = ")" * nesting_level
    
    full_string = ""
    for i in range(len(integers)):
        full_string += parens[i]
        full_string += str(integers[i])
    full_string += parens[i+1]



    return full_string

T = int(input())
for t in range(T):
    s = input()
    print("Case #"+str(t+1)+":", solve(s))
