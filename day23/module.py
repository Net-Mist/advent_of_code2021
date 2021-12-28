import cython
import numpy as np
from cython import declare

DTYPE = np.intc

if cython.compiled:
    CORRIDOR_POSITION_FROM_ROOM_IDX = declare(cython.int[4], [2, 4, 6, 8])
    CORRIDOR_POSITION_FROM_CORRIDOR_IDX = declare(cython.int[7], [0, 1, 3, 5, 7, 9, 10])
    CORRIDOR_SIZE = declare(cython.int, 7)
    CORRIDOR_PADDING = declare(cython.int, 2)
    ROOM_SIZE = declare(cython.int, 4)
    STATE_SIZE = declare(cython.int, 23)
    PART = declare(cython.int, 2)  # part 1 or 2 of the exercise
else:
    CORRIDOR_POSITION_FROM_ROOM_IDX = [2, 4, 6, 8]
    CORRIDOR_POSITION_FROM_CORRIDOR_IDX = [0, 1, 3, 5, 7, 9, 10]
    CORRIDOR_SIZE = 7
    CORRIDOR_PADDING = 2
    ROOM_SIZE = 4
    PART = 2  # part 1 or 2 of the exercise


def change_to_part1() -> None:
    global PART, ROOM_SIZE, STATE_SIZE
    PART = 1
    ROOM_SIZE = 2
    STATE_SIZE = 15


def get_init_state(file: str) -> np.ndarray:
    with open(file) as f:
        lines = f.readlines()
    if PART == 2:
        # insert
        #  #D#C#B#A#
        #  #D#B#A#C#
        lines = lines[:-2] + ["  #D#C#B#A#", "  #D#B#A#C#"] + lines[-2:]
    # state = 7 values for corridor, then 4 times 2 or 4 values for the rooms
    s_to_int = {"A": 1, "B": 2, "C": 3, "D": 4}

    init_state = [0] * 7 + [s_to_int[lines[2 + i][3 + 2 * c]] for c in range(4) for i in range(ROOM_SIZE)]

    return np.array(
        init_state,
        dtype=DTYPE,
    )


def array_to_display(a: np.ndarray) -> None:
    print(f"{a[0]}{a[1]}.{a[2]}.{a[3]}.{a[4]}.{a[5]}{a[6]}")
    print(f"  {a[7]} {a[11]} {a[15]} {a[19]}")
    print(f"  {a[7+1]} {a[11+1]} {a[15+1]} {a[19+1]}")
    print(f"  {a[7+2]} {a[11+2]} {a[15+2]} {a[19+2]}")
    print(f"  {a[7+3]} {a[11+3]} {a[15+3]} {a[19+3]}")


def reachable_corridor_from_room(room: cython.int, state: cython.int[:]) -> list:
    reachable_corridor = []
    for i in range(CORRIDOR_PADDING + room, CORRIDOR_SIZE):
        if state[i] == 0:
            reachable_corridor.append(i)
        else:
            break
    for i in range(CORRIDOR_PADDING - 1 + room, -1, -1):
        if state[i] == 0:
            reachable_corridor.append(i)
        else:
            break
    return reachable_corridor


def reachable_room_from_corridor(corridor: cython.int, state: cython.int[:]) -> list:
    # ############
    # 01.2.3.4.56#
    # ##0#1#2#3###
    reachable_room = []
    # going forward
    for i in range(corridor, CORRIDOR_SIZE - CORRIDOR_PADDING):
        if i != 0:
            reachable_room.append(i - 1)
        if state[i + 1] != 0:
            break
    # going backward
    for i in range(corridor, CORRIDOR_PADDING - 1, -1):
        if i != 6:
            reachable_room.append(i - 2)
        if state[i - 1] != 0:
            break
    return reachable_room


@cython.boundscheck(False)
@cython.wraparound(False)
def idx_first_elem_in_room(room: cython.int, state: cython.int[:]) -> cython.int:
    """return a number between 0 and ROOM_SIZE corresponding of the id of the first element from the corridor
    If room is empty returns -1
    """
    room_idx = CORRIDOR_SIZE + room * ROOM_SIZE

    for i in range(ROOM_SIZE):
        if state[room_idx + i] != 0:
            return i
    return -1


def move_to_corridor(room: cython.int, corridor: cython.int, state: cython.int[:], cost: cython.long) -> tuple:
    if all_ok_in_room(room, state):
        return state, cost
    id = idx_first_elem_in_room(room, state)
    if id == -1:
        return state, cost
    new_state = state.copy()
    e_id = CORRIDOR_SIZE + room * ROOM_SIZE + id
    new_state[e_id] = 0
    new_state[corridor] = state[e_id]

    new_cost = 1 + id  # cost to go out of the room
    new_cost += abs(CORRIDOR_POSITION_FROM_CORRIDOR_IDX[corridor] - CORRIDOR_POSITION_FROM_ROOM_IDX[room])
    new_cost = new_cost * 10 ** (new_state[corridor] - 1)

    return new_state, cost + new_cost


@cython.boundscheck(False)
@cython.wraparound(False)
def all_ok_in_room(room: cython.int, state: cython.int[:]) -> cython.char:
    first_element_index = CORRIDOR_SIZE + room * ROOM_SIZE
    for i in range(ROOM_SIZE):
        e = first_element_index + i
        if state[e] != room + 1 and state[e] != 0:
            return False
    return True


@cython.boundscheck(False)
@cython.wraparound(False)
def optimize(state: cython.int[:], cost: cython.long) -> tuple:
    # search for element in rooms than can directly go in the good room
    changed_state = True
    while changed_state:
        changed_state = False

        for room in range(4):
            id: cython.int = idx_first_elem_in_room(room, state)
            if id == -1:
                continue
            id_e = CORRIDOR_SIZE + room * ROOM_SIZE + id
            if state[id_e] == room + 1:
                continue
            dest_room: cython.int = state[id_e] - 1
            # it can be interesting to move id_e from room to dest_room
            if not all_ok_in_room(dest_room, state):
                continue
            # check path between both room
            first_room: cython.int = min(room, dest_room)
            last_room: cython.int = max(room, dest_room)

            not_ok = False
            for i in range(first_room + 2, last_room + 2):
                if state[i] != 0:
                    not_ok = True
                    break
            if not_ok:
                continue

            # move element
            dest_id: cython.int = idx_first_elem_in_room(dest_room, state)
            if dest_id == -1:
                dest_id = ROOM_SIZE - 1
            else:
                dest_id -= 1

            new_cost: cython.long = dest_id + 1 + id + 1 + abs(room - dest_room) * 2
            new_cost *= 10 ** (state[id_e] - 1)

            state[CORRIDOR_SIZE + dest_room * ROOM_SIZE + dest_id] = state[id_e]
            state[id_e] = 0

            cost += new_cost
            changed_state = True

        # check for element in corridor that can be put in room
        for corridor_id in range(7):
            if state[corridor_id] == 0:
                continue
            dest_room = state[corridor_id] - 1
            if not all_ok_in_room(dest_room, state):
                continue
            if dest_room not in reachable_room_from_corridor(corridor_id, state):
                continue
            # move inside room
            dest_id = idx_first_elem_in_room(dest_room, state)
            if dest_id == -1:
                dest_id = ROOM_SIZE - 1
            else:
                dest_id -= 1
            new_cost = dest_id + 1 + abs(2 + dest_room * 2 - CORRIDOR_POSITION_FROM_CORRIDOR_IDX[corridor_id])
            new_cost *= 10 ** (state[corridor_id] - 1)

            state[CORRIDOR_SIZE + dest_room * ROOM_SIZE + dest_id] = state[corridor_id]
            state[corridor_id] = 0
            cost += new_cost
            changed_state = True
    return state, cost


def check_end(state: cython.int[:]) -> bool:
    for i in range(7):
        if state[i] != 0:
            return False
    for i in range(4):
        for j in range(ROOM_SIZE):
            if state[7 + ROOM_SIZE * i + j] != i + 1:
                return False
    return True


def day23() -> int:
    init_state = get_init_state("input.txt")

    states = {tuple(init_state): [[], init_state, 0]}
    min_cost = 10000000
    while states:
        new_states = {}
        for item in states.values():
            old_states, state, cost = item
            for room in range(4):
                for corridor in reachable_corridor_from_room(room, state):
                    new_state, new_cost = optimize(*move_to_corridor(room, corridor, state, cost))

                    if cost == new_cost:
                        continue

                    if check_end(new_state):
                        if new_cost < min_cost:
                            min_cost = new_cost
                    else:
                        encoded = tuple(new_state)
                        if encoded not in new_states:
                            new_states[encoded] = [old_states + [new_state], new_state, new_cost]
                        else:
                            previous_cost = new_states[encoded][2]
                            if new_cost < previous_cost:
                                new_states[encoded] = [old_states + [new_state], new_state, new_cost]
        states = new_states
    return min_cost
