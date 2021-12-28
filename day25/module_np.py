import numpy as np


def move_right(map: np.ndarray) -> tuple:
    translated_map = np.concatenate([map[:, -1:], map[:, :-1]], axis=1)
    moved = (translated_map == 1) & (map == 0)
    init_map_position = np.concatenate([moved[:, 1:], moved[:, :1]], axis=1)
    map[init_map_position] = 0
    map[moved] = 1
    return map, moved.sum() != 0


def move_down(map: np.ndarray) -> tuple:
    translated_map = np.concatenate([map[-1:, :], map[:-1, :]])
    moved = (translated_map == 2) & (map == 0)
    init_map_position = np.concatenate([moved[1:, :], moved[:1, :]])
    map[init_map_position] = 0
    map[moved] = 2
    return map, moved.sum() != 0
