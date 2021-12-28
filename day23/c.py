import time

from module import change_to_part1, day23

# from module_c import change_to_part1, day23

t = time.time()
min_cost = day23()
print("part2:", min_cost)
print(time.time() - t, "seconds")

change_to_part1()
t = time.time()
min_cost = day23()
print("part1:", min_cost)
print(time.time() - t, "seconds")
