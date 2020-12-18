import numpy as np
with open("day13.txt") as f:
    lines = f.readlines()

earliest = int(lines[0])
departures = []
for i, departure in enumerate(lines[1].split(",")):
    if departure!="x":
        departures.append((i, int(departure)))

waiting_time = 1e6
bus_id = None
for departure in departures:
    departure = departure[1]
    new = departure - earliest % departure
    if new < waiting_time:
        waiting_time = new
        bus_id = departure
print(bus_id*waiting_time)


time = departures[0][1]
multiplier = 1

done = []
while True:
    valid = True
    for i, departure in departures:
        offset = (time + i) % departure
        if offset != 0:
            valid = False
            assert departure not in done
            break
        if departure not in done:
            done.append(departure)
            multiplier *= departure
    if valid:
        print(time)
        break
    time += multiplier
    # k += 1

