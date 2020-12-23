import re
import numpy as np
from prelude import fmap, join

with open("day14.txt") as f:
    lines = f.readlines()

def post(pre, mask):
    xs = int(mask.translate(str.maketrans({"0":"0","X":"1","1":"0"})),2)
    ones = int(mask.translate(str.maketrans({"0":"0","X":"0"})),2)
    zeros = int(mask.translate(str.maketrans({"0":"1","X":"0","1":"0"})),2)
    pre = pre & ~zeros
    pre = pre | ones
    return pre

addresses = {}
for line in lines:
    if line.startswith("mask"):
        mask = line[7:43]
    elif line.startswith("mem"):
        match = re.match("mem\[(.*?)\] = (.*)", line)
        address = int(match.group(1))
        pre = int(match.group(2))
        addresses[address] = post(pre, mask)
    else:
        raise ValueError("What")

print(sum(addresses.values()))
def write(addresses, mem, value):
    if "X" not in mem:
        address = int(join(mem), 2)
        addresses[address] = value
    for i, b in enumerate(mem):
        if b == "X":
            left = mem.copy()
            right = mem.copy()
            left[i] = "1"
            right[i] = "0"
            write(addresses, left, value)
            write(addresses, right, value)
            return

def apply_mask(address, mask):
    address_bits  = "{0:b}".format(address)
    mem = []
    for i, m in enumerate(mask[::-1]):
        if i >= len(address_bits):
            a = 0
        else:
            a = address_bits[-i-1]

        if m == "0":
            mem.append(a)
        elif m == "1":
            mem.append(1)
        elif m == "X":
            mem.append("X")
        else:
            raise ValueError("ha")
    mem = mem[::-1]

    return mem

addresses = {}
for line in lines:
    if line.startswith("mask"):
        mask = line[7:43]
    elif line.startswith("mem"):
        match = re.match("mem\[(.*?)\] = (.*)", line)
        address = int(match.group(1))
        value = int(match.group(2))
        mem = apply_mask(address, mask)
        write(addresses, mem, value)
    else:
        raise ValueError("What")
print(sum(addresses.values()))
