import re

import numpy as np

xs = []
ys = []
folds = []
with open("input.txt") as f:
    lines = f.readlines()
    for line in lines:
        if m := re.match(r"(\d+),(\d+)", line):
            xs.append(int(m.group(1)))
            ys.append(int(m.group(2)))
        if m := re.match(r"fold along ([xy])=(\d+)", line):
            folds.append((m.group(1), int(m.group(2))))

map = np.zeros((max(ys) + 1, max(xs) + 1), dtype=bool)
map[ys, xs] = True

first_fold = True
for fold in folds:
    if fold[0] == "x":
        map = map[:, : map.shape[1] // 2] + map[:, map.shape[1] // 2 + 1 :][:, ::-1]

    if fold[0] == "y":
        map = map[: map.shape[0] // 2, :] + map[map.shape[0] // 2 + 1 :, :][::-1, :]

    if first_fold:
        first_fold = False
        print("part1:", map.sum())

print("part2:")
for line in map:
    print("".join(["#" if c else " " for c in line]))
