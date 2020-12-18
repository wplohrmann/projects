with open("day7.txt") as f:
    lines = f.readlines()

mine = "shiny gold"
bag_rules = {}
for line in lines:
    words = line.split(" ")
    outer = " ".join(words[:2])
    bag_rules[outer] = {}
    if "no other bags" not in line:
        segments = " ".join(words[4:])
        for segment in segments.split(","):
            inner = " ".join(segment.strip(" ").split(" ")[1:3])
            number = int(segment.strip(" ").split(" ")[0])
            bag_rules[outer][inner] = number

count = 0
def count_bags_inside(outer):
    if bag_rules[outer] == {}:
        return 0
    else:
        return sum(number * (1 + count_bags_inside(inner)) for inner, number in bag_rules[outer].items())

print(count_bags_inside(mine))

