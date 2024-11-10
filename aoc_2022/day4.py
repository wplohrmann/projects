with open("day4.txt") as f:
    lines = f.read().splitlines()

score = 0
score2 = 0
for line in lines:
    l, r = line.split(",")
    l_l, l_r = map(int, l.split("-"))
    r_l, r_r = map(int, r.split("-"))
    l_set = set(range(l_l, l_r + 1))
    r_set = set(range(r_l, r_r+1))
    if l_set - r_set == set() or r_set - l_set == set():
        score += 1
    
    if len(l_set.intersection(r_set)) > 0:
        score2 += 1
print(score)
print(score2)
