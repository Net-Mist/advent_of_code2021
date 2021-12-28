import re

import numpy as np


def day5(diagonal: bool) -> int:
    x1s = []
    y1s = []
    x2s = []
    y2s = []

    with open("input.txt") as f:
        for line in f.readlines():
            match = re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line)
            x1, y1, x2, y2 = map(int, match.groups())
            x1s.append(x1)
            y1s.append(y1)
            x2s.append(x2)
            y2s.append(y2)

    # create grid
    x_max = max(x1s + x2s) + 1
    y_max = max(y1s + y2s) + 1
    grid = np.zeros((y_max, x_max))

    for x1, y1, x2, y2 in zip(x1s, y1s, x2s, y2s):
        # first case : horizontal/vertical lines
        if x1 == x2 or y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1

            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    grid[y, x] += 1
        elif diagonal:
            x_step = np.sign(x2 - x1)
            y_step = np.sign(y2 - y1)
            for x, y in zip(range(x1, x2 + x_step, x_step), range(y1, y2 + y_step, y_step)):
                grid[y, x] += 1

    # count
    return (grid >= 2).sum()


print("part1:", day5(False))
print("part2:", day5(True))
