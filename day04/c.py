import numpy as np

GRID_SIZE = 5


def read_bingo_grid(lines: list[str]) -> list[list[int]]:
    return [[int(n) for n in line.split()] for line in lines]


def bingo_step(grids: np.ndarray, checked_grids: np.ndarray, number: int) -> None:
    checked_grids[np.where(grids == number)] = True


def check_victory(check_grids: np.ndarray) -> set[int]:
    """return empty set if no victory, else set of id of the wining grids"""
    return set(np.where(check_grids.sum(axis=1).max(axis=1) == 5)[0]).union(
        np.where(check_grids.sum(axis=2).max(axis=1) == 5)[0]
    )


def sum_grid(grid: np.ndarray, checked_grid: np.ndarray) -> int:
    grid[checked_grid] = 0
    return grid.sum()


def main() -> None:
    with open("input.txt") as f:
        lines = f.readlines()
    random_numbers = [int(n) for n in lines[0].split(",")]
    grids = np.array([read_bingo_grid(lines[i : i + GRID_SIZE]) for i in range(2, len(lines), 1 + GRID_SIZE)])
    checked_grids = np.array([[[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)] for _ in range(len(grids))])

    win = False
    i = 0
    q1_done = False
    while not win:
        bingo_step(grids, checked_grids, random_numbers[i])
        winning_set = check_victory(checked_grids)
        if len(winning_set) == 1 and not q1_done:
            index = list(winning_set)[0]
            s = sum_grid(grids[index], checked_grids[index])
            print("part1:", s * random_numbers[i])
            q1_done = True
        if len(grids) == len(winning_set) + 1:
            index_last_to_win = list(set(range(len(grids))).difference(winning_set))[0]
        if len(grids) == len(winning_set):
            s = sum_grid(grids[index_last_to_win], checked_grids[index_last_to_win])
            print("part2:", random_numbers[i], s, random_numbers[i] * s)
            return
        i += 1


if __name__ == "__main__":
    main()
