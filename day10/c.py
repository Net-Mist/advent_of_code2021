from statistics import median

map_open_close = {"{": "}", "[": "]", "(": ")", "<": ">"}

score_part_1 = {
    "}": 1197,
    "]": 57,
    ")": 3,
    ">": 25137,
}

score_part_2 = {
    "}": 3,
    "]": 2,
    ")": 1,
    ">": 4,
}


def score_line(line: str) -> tuple[int, int]:
    """if the line is corrupted, then compute score of part 1, else compute score of part 2"""
    stack = []
    for c in line:
        if c in map_open_close:
            stack.append(c)
        else:
            try:
                e = stack.pop()
            except IndexError:
                return score_part_1[c], 0
            if map_open_close[e] != c:
                return score_part_1[c], 0
    # complete string
    s = 0
    for e in stack[::-1]:
        s *= 5
        s += score_part_2[map_open_close[e]]
    return 0, s


score_1 = 0
scores_2 = []

with open("input.txt") as f:
    for line in f.readlines():
        s1, s2 = score_line(line.strip())
        score_1 += s1
        if s2 != 0:
            scores_2.append(s2)
print("part1:", score_1)
print("part2:", median(scores_2))
