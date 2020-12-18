with open("day5.txt") as f:
    lines = f.readlines()
max_id = 0

def row_id(line):
    return int(line.replace("F", "0").replace("B", "1"), 2)

def col_id(line):
    return int(line.replace("R", "1").replace("L", "0"), 2)

part_two = True
seats = []

print(max(int(line.translate(str.maketrans("FBRL", "0110")), 2) for line in lines))

for line in lines:
    row = row_id(line[:7])
    col = col_id(line[7:-1])
    seat_id = 8 * row + col
    if part_two:
        seats.append(seat_id)
    if seat_id >= max_id:
        print("New highest:", seat_id, "Old:", max_id)
        max_id = seat_id

seats = sorted(seats)
previous = seats[0]-1
for seat in seats:
    if seat-1 != previous:
        print("Your seat:", seat-1)
    previous = seat

