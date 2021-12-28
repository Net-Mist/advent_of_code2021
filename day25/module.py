import cython
import numpy as np


def move_right(map: cython.int[:, ::1]) -> tuple:
    map_h = map.shape[0]
    map_w = map.shape[1]
    new_map: cython.int[:, :] = np.zeros_like(map)
    changed = False

    for x in range(map_w):
        for y in range(map_h):
            x_inc = x + 1 if x + 1 != map_w else 0
            if map[y, x] == 0:
                continue
            if map[y, x] == 1:
                if map[y, x_inc] == 0:
                    new_map[y, x_inc] = 1
                    changed = True
                else:
                    new_map[y, x] = 1
            else:
                new_map[y, x] = map[y, x]
    return new_map, changed


def move_down(map: cython.int[:, ::1]) -> tuple:
    map_h = map.shape[0]
    map_w = map.shape[1]
    new_map: cython.int[:, :] = np.zeros_like(map)
    changed = False

    for x in range(map_w):
        for y in range(map_h):
            y_inc = y + 1 if y + 1 != map_h else 0
            if map[y, x] == 0:
                continue
            if map[y, x] == 2:
                if map[y_inc, x] == 0:
                    new_map[y_inc, x] = 2
                    changed = True
                else:
                    new_map[y, x] = 2
            else:
                new_map[y, x] = map[y, x]
    return new_map, changed
