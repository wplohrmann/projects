from io_utils import from_grid, to_grid
from itertools import product
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from prelude import join
with open("day20.txt") as f:
    tiles=  f.read().split("\n\n")

ims = {}
titles = []
edges = defaultdict(lambda: [])
conv = lambda title: int(title.split()[1][:-1])
for tile in tiles:
    split = tile.splitlines()
    title, image = split[0], split[1:]
    title = conv(title)
    image = np.array(list(map(lambda line: np.array(list(line)), image)))
    ims[title] = image
    titles.append(title)
    edges[title].append(join(image[0]))
    edges[title].append(join(image[:,-1]))
    edges[title].append(join(image[-1]))
    edges[title].append(join(image[:,0]))

corner_titles = []
matches = defaultdict(lambda: [])
unique_edges = {}
for title in edges:
    unique_edges[title] = set(edges[title])
    for title2 in edges:
        if title2==title:
            continue
        for edge in edges[title2]:
            try:
                unique_edges[title].remove(edge)
            except KeyError:
                pass
            try:
                unique_edges[title].remove(edge[::-1])
            except KeyError:
                pass
    if len(unique_edges[title]) == 2:
        corner_titles.append(title)

p = np.prod(corner_titles)
print(p)

matches = defaultdict(lambda: [])
for title in edges:
    for title2 in edges:
        if title2==title:
            continue
        for edge in edges[title2]:
            if edge in edges[title]:
                matches[title].append(title2)
            elif edge[::-1] in edges[title]:
                matches[title].append(title2)

for title in matches:
    for neighbour in matches[title]:
        assert title in matches[neighbour]

w = 12
# w = 3

full = np.zeros((w*8,w*8), dtype=str)
full_titles = [[None for _ in range(w)] for _ in range(w)]
matched = set()
for title in corner_titles:
    indices = list(edges[title].index(edge) for edge in unique_edges[title])
    north = 0 in indices
    west = 3 in indices
    i = 0 if north else w-1
    j = 0 if west else w-1
    if not i == j == 0:
        continue
    full[i*8:(i+1)*8,j*8:(j+1)*8] = ims[title][1:-1,1:-1]
    full_titles[i][j] = title
    break
    matched.add(title)

def align(title, title2, index, index2):
    rotations = (2 + index - index2) % 4
    ims[title2] = np.rot90(ims[title2], -rotations)

    edges[title2] = []
    edges[title2].append(join(ims[title2][0]))
    edges[title2].append(join(ims[title2][:,-1]))
    edges[title2].append(join(ims[title2][-1]))
    edges[title2].append(join(ims[title2][:,0]))

    if not edges[title][index] == edges[title2][(2+index)%4]:
        if index % 2 == 0:
            ims[title2] = ims[title2][:,::-1]
        else:
            ims[title2] = ims[title2][::-1,:]
    else:
        return

    edges[title2] = []
    edges[title2].append(join(ims[title2][0]))
    edges[title2].append(join(ims[title2][:,-1]))
    edges[title2].append(join(ims[title2][-1]))
    edges[title2].append(join(ims[title2][:,0]))

    if not edges[title][index] == edges[title2][(2+index)%4]:
        import pdb; pdb.set_trace()
    return

for i,j  in product(range(w), range(w)):
    title = full_titles[i][j]
    if title is None:
        import pdb; pdb.set_trace()
    for title2 in matches[title]:
        if title2 in matched:
            continue
        for index2, edge in enumerate(edges[title2]):
            if edge in edges[title]:
                index = edges[title].index(edge)
            elif edge[::-1] in edges[title]:
                index = edges[title].index(edge[::-1])
            else:
                continue

            if index == 0:
                n_i = i-1
                n_j = j
            elif index == 1:
                n_j = j+1
                n_i = i
            elif index == 2:
                n_i = i+1
                n_j = j
            elif index == 3:
                n_j = j-1
                n_i = i
            else:
                import pdb; pdb.set_trace()
                raise ValueError("Whoops!")
            if n_i < 0 or n_j < 0:
                import pdb; pdb.set_trace()
            align(title, title2, index, index2)
            if not edges[title][index] == edges[title2][(index+2)%4]:
                import pdb; pdb.set_trace()
            full[n_i*8:(n_i+1)*8,n_j*8:(n_j+1)*8] = ims[title2][1:-1,1:-1]

            full_titles[n_i][n_j] = title2
            matched.add(title2)
            break

kernel = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
print(from_grid(full))
kernel  = (to_grid(kernel)=="#").astype(int)
from scipy.signal import correlate
max_dragons = None
full = np.flipud(full)
for _ in range(4):
    convolved = correlate(full=="#", kernel, mode="valid")
    num_dragons = np.sum(convolved==np.sum(kernel))
    if num_dragons != 0:
        assert max_dragons is None
        max_dragons = num_dragons
    full = np.rot90(full)
print(np.sum(full=="#") - np.sum(kernel) * max_dragons)

