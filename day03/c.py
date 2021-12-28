import numpy as np

with open("input.txt") as f:
    grid = np.array([[int(c) for c in line.strip()] for line in f.readlines()])

n_numbers, n_bits = grid.shape

gamma_bits = grid.sum(axis=0) / n_numbers > 0.5
gamma = sum(b * 2 ** (n_bits - 1 - i) for i, b in enumerate(gamma_bits))
epsilon_bits = ~gamma_bits
epsilon = sum(b * 2 ** (n_bits - 1 - i) for i, b in enumerate(epsilon_bits))

print("part1:", gamma * epsilon)

new_grid = grid
for i in range(n_bits):
    n_numbers = new_grid.shape[0]
    most_freq = int(new_grid[:, i].sum() / n_numbers >= 0.5)
    new_grid = new_grid[np.where(new_grid[:, i] == most_freq)]
oxygen = sum(b * 2 ** (n_bits - 1 - i) for i, b in enumerate(new_grid[0]))

new_grid = grid
for i in range(n_bits):
    n_numbers = new_grid.shape[0]
    if n_numbers == 1:
        break
    most_freq = int(new_grid[:, i].sum() / n_numbers >= 0.5)
    new_grid = new_grid[np.where(new_grid[:, i] != most_freq)]
co2 = sum(b * 2 ** (n_bits - 1 - i) for i, b in enumerate(new_grid[0]))

print("part2:", oxygen * co2)
