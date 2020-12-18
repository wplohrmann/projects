import re

rule_pattern = "(.*?)-(.*?) (.): (.*)$"

n = 0
while True:
    try:
        s = input()
    except EOFError:
        break

    match = re.search(rule_pattern, s)
    mn, mx, c, t = match.group(1), match.group(2), match.group(3), match.group(4)
    mn = int(mn)
    mx = int(mx)
    if False: # Part 1
        count_c = t.count(c)
        if mn <= count_c <= mx: n += 1
    else: # Part 2
        if (t[mn-1] == c) != (t[mx-1] == c): n += 1

print(n)
