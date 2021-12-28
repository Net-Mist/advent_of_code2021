from collections import Counter


def day14(n_steps: int) -> int:
    instructions = {}

    pairs_count = Counter()
    with open("input.txt") as f:
        lines = f.readlines()
    polymer = lines[0].strip()
    for line in lines[2:]:
        instructions[line.split()[0]] = line.split()[2]

    first_c = polymer[0]
    last_c = polymer[-1]

    for i in range(len(polymer) - 1):
        pairs_count[polymer[i : i + 2]] += 1

    for _ in range(n_steps):
        new_pairs_count = Counter()
        for k, v in pairs_count.items():
            if k in instructions:
                new_pairs_count[k[0] + instructions[k]] += v
                new_pairs_count[instructions[k] + k[1]] += v
        pairs_count = new_pairs_count

    caracter_counter = Counter()
    for k, v in pairs_count.items():
        caracter_counter[k[0]] += v
        caracter_counter[k[1]] += v
    caracter_counter[first_c] += 1
    caracter_counter[last_c] += 1

    M = max(caracter_counter.values()) // 2
    m = min(caracter_counter.values()) // 2
    return M - m


print("part1:", day14(10))
print("part2:", day14(40))
