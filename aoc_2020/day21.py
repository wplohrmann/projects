import re
from scipy.signal import convolve
import numpy as np
from itertools import product
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
from io_utils import from_grid, to_grid

with open("day21.txt") as f:
    lines = f.readlines()

allergens = set()
full_ingredients=  set()
maybe_allergens = {}
counts = Counter()
for line in lines:
    i, a = re.match("(.*) \(contains (.*)\)", line).groups()
    is_allergen = False
    these_ingredients = set(i.split())
    these_allergens = set(a.replace(",","").replace(")","").split())
    counts += Counter(these_ingredients)
    for a in these_allergens:
        if a in maybe_allergens:
            maybe_allergens[a] = these_ingredients.intersection(maybe_allergens[a])
        else:
            maybe_allergens[a] = these_ingredients

    allergens = allergens.union(these_allergens)
    full_ingredients = full_ingredients.union(these_ingredients)

not_allergic = full_ingredients - set.union(*maybe_allergens.values())
c = sum(counts[i] for i in not_allergic)
print(c)

matched_allergens = {}
while len(matched_allergens) != len(maybe_allergens):
    for a in maybe_allergens:
        if len(maybe_allergens[a]) == 1:
            matched_allergens[a] = maybe_allergens[a].pop()
            for a2 in maybe_allergens:
                if a==a2:
                    continue
                try:
                    maybe_allergens[a2].remove(matched_allergens[a])
                except KeyError:
                    pass
stock = map(lambda x: x[1], sorted(matched_allergens.items(), key=lambda x: x[0]))
print(*stock, sep=",")

