import re

p = re.compile(r"\[[0-9]+,[0-9]+\]")

DEF ascii_0 = 48
DEF ascii_9 = 57

cdef find_full_int(str number, int i):
    if ascii_0 <=  number[i + 1] <= ascii_9:
        return int(number[i : i + 2]), i, i + 1
    if ascii_0 <=  number[i - 1] <= ascii_9:
        return int(number[i - 1 : i + 1]), i - 1, i
    return int(number[i]), i, i


cdef explode(number: str):
    inner_level = 0
    number_left_position = -1
    cdef char c
    cdef int i, j
    cdef int left_number, start_left_n, end_left_n
    cdef int right_number, start_right_n, end_right_n
    cdef int start_right_inc, end_right_inc, right_inc
    cdef int left_inc, start_left_inc, end_left_inc
    cdef str previous_n, end_n

    for i, c in enumerate(number):
        if c == 91: #"["
            inner_level += 1
            continue
        if c == 93: #"]"
            inner_level -= 1
            continue
        if c == 44: # ","
            continue
        if inner_level <= 4:
            number_left_position = i
            continue

        # explode
        left_number, start_left_n, end_left_n = find_full_int(number, i)
        right_number, start_right_n, end_right_n = find_full_int(number, end_left_n + 2)

        # explore the string until a number to increment
        start_right_inc = -1
        end_right_inc = -1
        for j in range(end_right_n + 1, len(number)):
            if number[j] >= 48 and  number[j] <= 57:
                right_inc, start_right_inc, end_right_inc = find_full_int(number, j)
                break

        if number_left_position == -1:
            previous_n = number[: start_left_n - 1]
        else:
            left_inc, start_left_inc, end_left_inc = find_full_int(number, number_left_position)
            previous_n = (
                number[:start_left_inc] + str(left_inc + left_number) + number[end_left_inc + 1 : start_left_n - 1]
            )

        if start_right_inc == -1:
            end_n = number[end_right_n + 2 :]
        else:
            end_n = (
                number[end_right_n + 2 : start_right_inc] + str(right_inc + right_number) + number[end_right_inc + 1 :]
            )

        return previous_n + "0" + end_n, True
    return number, False


cdef split(str number):
    cdef int i
    cdef char c
    cdef int n, start_n, end_n
    for i, c in enumerate(number):
        if c >= 48 and  c <= 57:
            n, start_n, end_n = find_full_int(number, i)
            if n >= 10:
                return (
                    number[:start_n] + "[" + str(n // 2) + "," + str(n // 2 + n % 2) + "]" + number[end_n + 1 :],
                    True,
                )
    return number, False


cdef str process(str number):
    cdef char did_something
    did_something = True
    while did_something:
        number, did_something = explode(number)
        if did_something:
            continue
        number, did_something = split(number)
        if did_something:
            continue
        return number


cdef str addition(str n1, str n2):
    return process("[" + n1 + "," + n2 + "]")

cdef int magnitude(str number):
    cdef int idx_diff
    cdef str a, b, r
    while "[" in number:
        idx_diff = 0
        for m in p.finditer(number):
            a, b = m.group()[1:-1].split(",")
            r = str(3 * int(a) + 2 * int(b))
            number = number[: m.start() - idx_diff] + r + number[m.end() - idx_diff :]
            idx_diff += m.end() - m.start() - len(r)
    return int(number)

cpdef day18():
    cdef int i1, i2
    cdef list numbers
    cdef str n1, n2
    m = 0
    with open("input.txt") as f:
        numbers = [n.strip() for n in f.readlines()]
    for i1, n1 in enumerate(numbers):
        for i2, n2 in enumerate(numbers):
            if i1 == i2:
                continue
            m = max(m, magnitude(addition(n1, n2)))

    n = numbers[0]
    for n1 in numbers[1:]:
        n = addition(n, n1)

    return magnitude(n), m
