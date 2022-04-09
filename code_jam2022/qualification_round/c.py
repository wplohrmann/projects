def solve(dice):
    max_possible = min(len(dice), max(dice))
    dice = sorted(dice)[-max_possible:]
    while True:
        for i in range(max_possible):
            if dice[i] < i+1:
                max_possible -= 1
                dice = dice[1:]
                break
        else:
            return max_possible

T = int(input())
for t in range(T):
    input()
    dice = [int(x) for x in input().split()]
    print(f"Case #{t+1}:", solve(dice))
