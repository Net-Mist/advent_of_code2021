import numpy as np

ctypedef unsigned long[:,:] MAP_t
ctypedef unsigned long[:] CONVERT_t

cdef MAP_t pad(MAP_t map, long value):
    return np.pad(map, ((1, 1), (1, 1)), constant_values=value)

cpdef int convert_to_index(MAP_t submap) nogil:
    cdef int i, j, s
    s = 0
    for i in range(3):
        for j in range(3):
            s = s*2 + submap[i, j]
    return s

cdef enhance(MAP_t map, int[512] convert, long inf_value):
    cdef long x, y
    cdef int index
    cdef MAP_t sub_map, new_map
    # start by padding map
    map = pad(map, inf_value)
    map = pad(map, inf_value)
    inf_value = 1 - inf_value

    new_map = np.zeros_like(map, dtype=np.uint)
    max_x = map.shape[0] - 1
    max_y = map.shape[1] - 1

    for x in range(1, max_x):
        for y in range(1, max_y):
            new_map[x, y] = convert[convert_to_index(map[x - 1 : x + 2, y - 1 : y + 2])]
    return new_map[1:-1, 1:-1], inf_value

cpdef day20():
    with open("input.txt") as f:
        lines = f.readlines()
    cdef int[512] convert = [0 if c == "." else 1 for c in lines[0].strip()]
    map = np.array([[0 if c == "." else 1 for c in line.strip()] for line in lines[2:]], dtype=np.uint)

    inf_value = 0
    for i in range(2):
        map, inf_value = enhance(map, convert, inf_value)

    print("part1:", np.sum(map))
    for i in range(48):
        map, inf_value = enhance(map, convert, inf_value)

    print("part2:", np.sum(map))
