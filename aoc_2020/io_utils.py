import numpy as np
def to_grid(s, ones="#"):
    image = np.stack(list(map(lambda line: np.array(list(line))==ones, s.splitlines())))

    return image


def from_grid(arr, ones="#", zeros="."):
    return "\n".join(map(lambda l: "".join(l), arr))


