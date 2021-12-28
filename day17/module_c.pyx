from libcpp.vector cimport vector


cdef int sign(int x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def compute_valid_x(int target_x_min, int target_x_max):
    cdef int x, speed_x, previous_x
    cdef vector[int] valid_x
    for start_speed_x in range(target_x_max + 1):
        x = 0
        speed_x = start_speed_x
        previous_x = target_x_max + 1
        while True:
            x += speed_x
            speed_x = speed_x - sign(speed_x)
            if x >= target_x_min and x <= target_x_max:
                valid_x.push_back(start_speed_x)
                break
            if x > target_x_max or x == previous_x:
                break
            previous_x = x
    return valid_x

def compute_valid_xy(int target_y_min, int target_y_max, int target_x_max, int target_x_min, vector[int] valid_x):
    cdef int x, y, speed_x, speed_y, start_speed_x
    cdef vector[int] valid_y
    for start_speed_x in valid_x:
        for start_speed_y in range(target_y_min, -target_y_min):
            x, y = 0, 0
            speed_x = start_speed_x
            speed_y = start_speed_y
            while True:
                x += speed_x
                y += speed_y
                speed_x -= sign(speed_x)
                speed_y -= 1
                if target_x_min <= x <= target_x_max and target_y_min <= y <= target_y_max:
                    valid_y.push_back(start_speed_y)
                    break
                if y < target_y_min:
                    break
                if x > target_x_max:
                    break
    return valid_y
