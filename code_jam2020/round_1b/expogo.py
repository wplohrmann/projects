def solve(x, y):
    """

    >>> solve(2, 3)
    SEN
    """
    solution = ""
    while x!=0 or y != 0:
        if (x+y)%2 == 0: # One exactly must be odd
            return None
        if x % 2 == 1: # Next step is east/west
            if x == 1 and y==0:
                solution += "E"
                x -= 1
            elif x == -1 and y==0:
                solution += "W"
                x += 1
            elif ((x-1)//2+y//2) % 2 == 0: # Both even or odd after going west
                x += 1 # This case may also fail but we'll figure it out in the next iteration
                solution += "W"
            else:
                x -= 1
                solution += "E"
        else: # Next step is north/south
            if y == 1 and x==0:
                solution += "N"
                y -= 1
            elif y == -1 and x==0:
                solution += "S"
                y += 1
            elif (x//2+(y-1)//2) % 2 == 0: # Both even or odd after going south
                y += 1 # This case may also fail but we'll figure it out later
                solution += "S"
            else:
                y -= 1
                solution += "N"
        if x%2 != 0 or y%2 != 0:
            return None
        x //= 2
        y //= 2

    # Convert bin_x bin_y to correct representation
    return solution

if __name__=="__main__":
    T = int(input())

    for t in range(T):
        x, y = map(int, input().split())
        solution = solve(x, y)
        if solution is None:
            print("Case #"+str(t+1)+":", "IMPOSSIBLE")
        else:
            print("Case #"+str(t+1)+":", solution)
