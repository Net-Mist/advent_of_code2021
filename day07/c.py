import numpy as np

with open("input.txt") as f:
    array = np.array([int(i) for i in f.readline().split(",")])

print("part1:", int(np.absolute(array - np.median(array)).sum()))

# part 2
distances_to_cost = [i * (i + 1) / 2 for i in range(array.max() + 1)]
previous_cost = np.inf
for i in range(array.max()):
    distances = np.absolute(array - i)
    cost = sum(distances_to_cost[i] for i in distances)
    if cost > previous_cost:
        break
    previous_cost = cost
print("part2:", int(previous_cost))
