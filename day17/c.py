import re
import time

from module import compute_valid_x, compute_valid_xy

# from module_c import compute_valid_x, compute_valid_xy
# from module_c2 import compute_valid_x, compute_valid_xy

# from module import compute_valid_x, compute_valid_xy

with open("input.txt") as f:
    m = re.match(r"target area: x=(-?[0-9]+)\.\.(-?[0-9]+), y=(-?[0-9]+)\.\.(-?[0-9]+)", f.readline())
    target_x_min, target_x_max, target_y_min, target_y_max = (int(i) for i in m.groups())

# compute valid initial speed along x axis
start_time = time.time()
valid_x = compute_valid_x(target_x_min, target_x_max)
valid_y = compute_valid_xy(target_y_min, target_y_max, target_x_max, target_x_min, valid_x)


start_speed_y = max(valid_y)
max_y = 0
speed_y = start_speed_y
while speed_y > 0:
    max_y += speed_y
    speed_y -= 1
print("part1:", max_y)
print("part2:", len(valid_y))

assert max_y == 2628
assert len(valid_y) == 1334
print("time (in seconds):", time.time() - start_time)
