with open('day2.txt') as f:
    lines = f.read().splitlines()
    
score = 0
hims = ["A", "B", "C"]
mes = ["X", "Y", "Z"]
for line in lines:
    him, me = line.split()
    him = hims.index(him)
    me = mes.index(me)
    score += (me + 1)
    if (him - me) % 3 == 0: # Draw
        score += 3
    if (him - me) % 3 == 1: # I lose
        pass
    if (him - me) % 3 == 2: # I win
        score += 6
print(score)

score = 0
for line in lines:
    him, me = line.split()
    him = hims.index(him)
    me = mes.index(me)
    if me == 0: # Lose
        me = (him - 1) % 3
    elif me == 1: # Draw
        score += 3
        me = him
    elif me == 2: # Draw
        score += 6
        me = (him + 1) % 3

    score += (me + 1)
print(score)
