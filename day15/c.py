import time

import numpy as np
from module import find_s

# from module_c import find_s


with open("input.txt") as f:
    map = np.array([[int(c) for c in line[:-1]] for line in f.readlines()], dtype=np.intc)


def day15(map: np.ndarray, full_map: bool) -> tuple[int, int]:
    if full_map:
        map = np.concatenate([(map + i) % 9 for i in range(5)], axis=0)
        map = np.concatenate([(map + i) % 9 for i in range(5)], axis=1)
        map[np.where(map == 0)] = 9

    scores = np.zeros_like(map, dtype=np.intc) - 1
    max_position = map.shape[0]
    ts = time.time()
    return find_s(scores, max_position, map), time.time() - ts


s, t = day15(map, False)
print("part1:", s, "in", t, "seconds")

s, t = day15(map, True)
print("part2:", s, "in", t, "seconds")
