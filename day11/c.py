import numpy as np

with open("input.txt") as f:
    map = np.array([[int(c) for c in line.strip()] for line in f.readlines()])
size = len(map)


def increase_neighbour(map: np.ndarray, flashes: np.ndarray, x: int, y: int) -> None:
    for xn in range(max(0, x - 1), min(x + 2, size)):
        for yn in range(max(0, y - 1), min(y + 2, size)):
            if not flashes[xn, yn]:
                map[xn, yn] += 1


s = 0
for step in range(500):
    map = map + 1
    flashes = np.zeros_like(map)
    while (map > 9).sum() != 0:
        xs, ys = np.where(map > 9)
        map[xs, ys] = 0
        flashes[xs, ys] = 1
        for x, y in zip(xs, ys):
            increase_neighbour(map, flashes, x, y)
    s += flashes.sum()
    if step == 99:
        print("part1:", s)
    if flashes.sum() == 100:
        print("part2:", step + 1)
        break
