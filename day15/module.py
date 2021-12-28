from heapq import heappop, heappush

import numpy as np


def find_s(scores: np.ndarray, max_position: int, map: np.ndarray) -> int:
    score_and_position = []
    heappush(score_and_position, (0, 0, 0))

    while True:
        best_position = heappop(score_and_position)

        s = best_position[0]
        x = best_position[1]
        y = best_position[2]

        if scores[x, y] != -1:
            continue

        scores[x, y] = s

        if x == max_position - 1 and y == max_position - 1:
            return s

        if y + 1 < max_position and scores[x, y + 1] == -1:
            e = (s + map[x, y + 1], x, y + 1)
            heappush(score_and_position, e)
        if x + 1 < max_position and scores[x + 1, y] == -1:
            e = (s + map[x + 1, y], x + 1, y)
            heappush(score_and_position, e)
        if y - 1 >= 0 and scores[x, y - 1] == -1:
            e = (s + map[x, y - 1], x, y - 1)
            heappush(score_and_position, e)
        if x - 1 >= 0 and scores[x - 1, y] == -1:
            e = (s + map[x - 1, y], x - 1, y)
            heappush(score_and_position, e)
