with open("day7.txt") as f:
    lines = f.readlines()

mine = "shiny gold"
bag_rules = {}
for line in lines:
    words = line.split(" ")
    outer = " ".join(words[:2])
    bag_rules[outer] = []
    if "no other bags" not in line:
        segments = " ".join(words[4:])
        bag_rules[outer] = []
        for segment in segments.split(","):
            inner = " ".join(segment.strip(" ").split(" ")[1:3])
            bag_rules[outer].append(inner)

def allowed(outer, inner):
    print(outer, inner)
    if len(bag_rules[outer]) == 0:
        return False
    elif inner in bag_rules[outer]:
        return True
    else:
        return any([allowed(key, inner) for key in bag_rules[outer]])

count = 0
for key in bag_rules:
    if allowed(key, mine):
        count += 1

print(count)
