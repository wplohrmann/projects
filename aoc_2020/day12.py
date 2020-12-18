import numpy as np
with open("day12.txt") as f:
    lines = f.readlines()

east = 0
north = 0
direction = np.array([1, 0])

for line in lines:
    distance = int(line[1:])
    if line[0] == "N":
        north += distance
    elif line[0] == "E":
        east += distance
    elif line[0] == "W":
        east -= distance
    elif line[0] == "S":
        north -= distance
    elif line[0] == "F":
        east += direction[0] * distance
        north += direction[1] * distance
    elif line[0] == "R":
        angle=distance * np.pi/180
        kernel = np.array([[np.cos(angle), np.sin(angle)],[-np.sin(angle),np.cos(angle)]])
        direction = kernel @ direction
    elif line[0] == "L":
        angle=distance * np.pi/180
        kernel = np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle),np.cos(angle)]])
        direction = kernel @ direction
    else:
        print("What!", line)
    
print("Part 1:", round(abs(east) + abs(north)))

east = 0
north = 0
waypoint = np.array([10, 1])

for line in lines:
    distance = int(line[1:])
    if line[0] == "N":
        waypoint[1] += distance
    elif line[0] == "E":
        waypoint[0] += distance
    elif line[0] == "W":
        waypoint[0] -= distance
    elif line[0] == "S":
        waypoint[1] -= distance
    elif line[0] == "F":
        east += waypoint[0] * distance
        north += waypoint[1] * distance
    elif line[0] == "R":
        angle=distance * np.pi/180
        kernel = np.array([[np.cos(angle), np.sin(angle)],[-np.sin(angle),np.cos(angle)]])
        waypoint = kernel @ waypoint
    elif line[0] == "L":
        angle=distance * np.pi/180
        kernel = np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle),np.cos(angle)]])
        waypoint = kernel @ waypoint
    else:
        print("What!", line)
    
print("Part 2:", round(abs(east) + abs(north)))
