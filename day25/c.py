from time import time

import numpy as np
from module_np import move_down, move_right

# from module import move_down, move_right
# from module_c import move_down, move_right

str_to_number = {".": 0, ">": 1, "v": 2}
with open("input.txt") as f:
    lines = f.readlines()
map = np.array([[str_to_number[s] for s in line[:-1]] for line in lines], dtype=np.intc)


t = time()

changed = True
i = 0
while changed:
    i += 1
    changed = False
    map, changed_r = move_right(map)

    changed |= changed_r
    map, changed_d = move_down(map)
    changed |= changed_d
print("part1:", i)
print("no part 2")
print(time() - t, "seconds")
