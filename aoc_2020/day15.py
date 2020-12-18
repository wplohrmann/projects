from collections import defaultdict

numbers = [1,12,0,20,8,16]
# numbers = [0, 3, 6]
turns = defaultdict(lambda: [])
for i, n in enumerate(numbers):
    print("Saying", n)
    turns[n].append(i)
    last_spoken = n

while True:
    next_number = turns[last_spoken]
    if next_number == 0:
        pass
    elif len(next_number) == 1:
        next_number = 0
    elif len(next_number) > 1:
        next_number = next_number[-1] - next_number[-2]
    if len(turns[last_spoken]) > 10: # Or two, or whatever but you probably don't want to update too often
        turns[last_spoken] = turns[last_spoken][-2:]
    i += 1
    numbers.append(next_number)
    last_spoken = next_number
    turns[last_spoken].append(i)
    if i > 30000000:
        break
print(numbers[2019])
print(numbers[30000000-1])



