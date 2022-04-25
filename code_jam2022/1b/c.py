from random import shuffle

def solve():
    """
    The ordering doesn't matter
    """
    n = 8
    while True:
        guess = ["0" for i in range(8-n)] + ["1" for i in range(n)]
        shuffle(guess)
        print("".join(guess))
        n = int(input())
        if n == 0:
            return
        elif n == -1:
            return




T = int(input())
for t in range(T):
    solve()
