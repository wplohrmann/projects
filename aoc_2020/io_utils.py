import numpy as np
def to_grid(s):
    image = np.stack(list(map(lambda line: np.array(list(line)), s.splitlines())))

    return image


def from_grid(arr):
    return "\n".join(map(lambda l: "".join(l.astype(str)), arr))


