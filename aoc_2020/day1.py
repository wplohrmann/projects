from itertools import product
with open("day1.txt") as f:
    xs = set(map(int, f.readlines()))

print([x*(2020-x) for x in xs if 2020-x in xs][0])
xs.forEach(x => xs.includes(2020 - x) ? console.log(x * (2020-x)) : 0)

