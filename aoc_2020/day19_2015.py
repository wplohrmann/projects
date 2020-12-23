import re
from prelude import fmap

with open("day19_2015.txt") as f:
    rules, start = f.read().split("\n\n")
rules = list(map(lambda x: x.split(" => "), rules.splitlines()))
start = start.strip()

def apply(rule, molecule):
    molecules = set()
    for match in re.finditer(rule[0], molecule):
        new = molecule[:match.span()[0]] + rule[1] + molecule[match.span()[1]:]
        if new == "e" or "e" not in new:
            molecules.add(new)
    return molecules

def one_replacement(rules, molecule):
    return set.union(*list(apply(rule, molecule) for rule in rules))

print(len(one_replacement(rules, start)))

anti_rules = fmap(lambda x: x[::-1], rules)
# Path finding from end to e
# anti_rules = [["H", "e"], ["O", "e"], ["HO", "H"], ["OH", "H"], ["HH", "O"]]
# start = "HOHOHO"
path_lengths = {start: 0}
possibilities = set([start])
i = 0
while "e" not in path_lengths:
    i += 1
    new_molecules = set()
    for molecule in possibilities:
        transforms = one_replacement(anti_rules, molecule)
        new_molecules.update(transforms)
    possibilities = new_molecules
    max_len = 1e99
    possibilities -= path_lengths.keys()
    possibilities = {min(possibilities, key=len)}
    for molecule in possibilities:
        if len(molecule) < max_len:
            max_len = len(molecule)
        path_lengths[molecule] = i

print(path_lengths["e"])
