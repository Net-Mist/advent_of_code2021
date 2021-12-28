import re

import numpy as np

with open("input.txt") as f:
    lines = f.readlines()

cmds = []
for line in lines:
    m = re.match(r"(-?\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line)
    cmds.append((m.groups()[0],) + tuple(int(i) for i in m.groups()[1:]))

translate_vector = [50, 50, 50]
engine_grid = np.zeros((101, 101, 101), dtype=bool)

for cmd in cmds:
    value = cmd[0] == "on"
    x_min = max(0, cmd[1] + translate_vector[0])
    x_max = min(100, cmd[2] + translate_vector[0])
    y_min = max(0, cmd[3] + translate_vector[1])
    y_max = min(100, cmd[4] + translate_vector[1])
    z_min = max(0, cmd[5] + translate_vector[2])
    z_max = min(100, cmd[6] + translate_vector[2])
    engine_grid[x_min : x_max + 1, y_min : y_max + 1, z_min : z_max + 1] = value

print(engine_grid.sum())
