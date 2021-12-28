from collections import Counter


def day6(n_days: int) -> int:
    with open("input.txt") as f:
        fishes = map(int, f.readline().split(","))

    n_fish_per_day = Counter()

    for f in fishes:
        n_fish_per_day[f] += 1

    # simulate days
    for _ in range(n_days):
        new_n_fish_per_day = {}
        for i in range(1, 9):
            new_n_fish_per_day[i - 1] = n_fish_per_day[i]
            n_new_fish = n_fish_per_day[0]
        new_n_fish_per_day[6] += n_new_fish
        new_n_fish_per_day[8] = n_new_fish
        n_fish_per_day = new_n_fish_per_day

    # count
    return sum(n_fish_per_day[i] for i in range(0, 9))


print("part1:", day6(80))
print("part2:", day6(256))
