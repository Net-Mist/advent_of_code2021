import numpy as np

# read map and pad with 9
map = []
with open("input.txt") as f:
    for line in f.readlines():
        map.append([9] + [int(c) for c in line[:-1]] + [9])
line_length = len(line) - 1
map = np.array([[9] * (line_length + 2)] + map + [[9] * (line_length + 2)])

# part 1 + find all minimum
r = 0
min_map = np.zeros_like(map)
for i in range(1, map.shape[0] - 1):
    for j in range(1, map.shape[1] - 1):
        submap = map[i - 1 : i + 2, j - 1 : j + 2]
        if (
            submap[1, 1] < submap[0, 1]
            and submap[1, 1] < submap[2, 1]
            and submap[1, 1] < submap[1, 0]
            and submap[1, 1] < submap[1, 2]
        ):
            r += 1 + int(submap[1, 1])
            min_map[i, j] = 1
print("part1:", r)


def fill_basin(basin: np.ndarray, map: np.ndarray) -> None:
    # basin == 1 : to check
    # basin == 2 : sure, basin
    # basin == 3 : sure not basin
    while True:
        xs, ys = np.where(basin == 1)
        if not len(xs):
            return
        for x, y in zip(xs, ys):
            if map[x, y] == 9:
                basin[x, y] = 3
            else:
                basin[x, y] = 2
                basin[x - 1, y] = max(1, basin[x - 1, y])
                basin[x + 1, y] = max(1, basin[x + 1, y])
                basin[x, y - 1] = max(1, basin[x, y - 1])
                basin[x, y + 1] = max(1, basin[x, y + 1])


basin_sizes = []
explored = np.zeros_like(min_map)
for x, y in zip(*np.where(min_map == 1)):
    if explored[x, y]:
        continue
    basin = np.zeros_like(min_map)
    basin[x, y] = 1
    fill_basin(basin, map)
    basin_sizes.append((basin == 2).sum())
    explored = explored + (basin == 2)

basin_sizes.sort()
a, b, c = basin_sizes[-3:]
print("part2:", a * b * c)
