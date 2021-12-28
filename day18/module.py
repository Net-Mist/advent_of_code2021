import re

p = re.compile(r"\[[0-9]+,[0-9]+\]")

ascii_0 = ord("0")
ascii_9 = ord("9")


def find_full_int(number: str, i: int) -> tuple[int, int, int]:
    if ascii_0 <= ord(number[i + 1]) <= ascii_9:
        return int(number[i : i + 2]), i, i + 1
    if ascii_0 <= ord(number[i - 1]) <= ascii_9:
        return int(number[i - 1 : i + 1]), i - 1, i
    return int(number[i]), i, i


def explode(number: str) -> tuple[str, bool]:
    inner_level = 0
    number_left_position = -1
    for i, c in enumerate(number):
        if c == "[":
            inner_level += 1
            continue
        if c == "]":
            inner_level -= 1
            continue
        if c == ",":
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
            if ascii_0 <= ord(number[j]) <= ascii_9:
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


def split(number: str) -> tuple[str, bool]:
    for i, c in enumerate(number):
        if ascii_0 <= ord(c) <= ascii_9:
            n, start_n, end_n = find_full_int(number, i)
            if n >= 10:
                return (
                    number[:start_n] + "[" + str(n // 2) + "," + str(n // 2 + n % 2) + "]" + number[end_n + 1 :],
                    True,
                )
    return number, False


def process(number: str) -> str:
    did_something = True
    while did_something:
        number, did_something = explode(number)
        if did_something:
            continue
        number, did_something = split(number)
        if did_something:
            continue
        return number


def addition(n1: str, n2: str) -> str:
    return process("[" + n1 + "," + n2 + "]")


def magnitude(number: str) -> int:
    while "[" in number:
        idx_diff = 0
        for m in p.finditer(number):
            a, b = m.group()[1:-1].split(",")
            r = str(3 * int(a) + 2 * int(b))
            number = number[: m.start() - idx_diff] + r + number[m.end() - idx_diff :]
            idx_diff += m.end() - m.start() - len(r)
    return int(number)


def day18() -> tuple[int, int]:
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
