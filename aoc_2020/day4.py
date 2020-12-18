import re
with open("day4.txt") as f:
    lines = f.readlines()

valid_passes = 0
required_fields = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
part_two = True

present = set()
for line in lines:
    if line == "\n":
        if required_fields.issubset(present):
            valid_passes += 1
        present = set()
        continue
    entries = line.split(" ")
    for entry in entries:
        if part_two:
            key = entry[:3]
            value = entry[4:]
            value = value.strip("\n")
            if key == "byr":
                if 1920 <= int(value) <= 2002:
                    present.add(key)
            elif key == "iyr":
                if 2010 <= int(value) <= 2020:
                    present.add(key)
            elif key == "eyr":
                if 2020 <= int(value) <= 2030:
                    present.add(key)
            elif key == "hgt":
                match = re.match("(\d.*?)(cm|in)", value)
                if match:
                    height = int(match.group(1))
                    if match.group(2) == "cm":
                        if 150 <= height <= 193:
                            present.add(key)
                    elif match.group(2) == "in":
                        if 59 <= height <= 76:
                            present.add(key)
            elif key == "hcl":
                match = re.match("#[0-9a-f]{6}", value)
                if match:
                    present.add(key)
            elif key == "ecl":
                match = re.match("amb|blu|brn|gry|grn|hzl|oth", value)
                if match:
                    present.add(key)
            elif key == "pid":
                match = re.match("[0-9]{9}", value)
                if match:
                    present.add(key)
            elif key == "cid":
                pass
            else:
                print(key, value)
        else:
            present.add(entry[:3])

print(valid_passes)
