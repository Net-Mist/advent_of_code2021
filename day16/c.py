import functools


def hex_to_bin(hex_number: str) -> str:
    return bin(int(hex_number, 16))[2:].zfill(len(hex_number) * 4)


def bin_to_dec(bin_number: str) -> int:
    return int(bin_number, 2)


version_sum = 0


def parse_packet(binary_transmission: str) -> tuple[int, int]:
    """parse the packet and return the index of end of packet and the literal"""
    global version_sum
    version = bin_to_dec(binary_transmission[:3])
    type_id = bin_to_dec(binary_transmission[3:6])
    version_sum += version
    if type_id == 4:
        # then literal value
        # read bits 5 per 5
        end_of_literal = False
        i = 0
        binary_number = ""
        while not end_of_literal:
            group = binary_transmission[6 + 5 * i : 6 + 5 * (i + 1)]
            if group[0] == "0":
                end_of_literal = True
            binary_number += group[1:]
            i += 1
        return 6 + 5 * i, bin_to_dec(binary_number)
    else:
        # operator
        final_i = 0
        numbers = []
        length_type_id = binary_transmission[6]
        if length_type_id == "0":
            total_length = bin_to_dec(binary_transmission[7 : 7 + 15])
            while final_i < total_length:
                i, n = parse_packet(binary_transmission[7 + 15 + final_i :])
                final_i += i
                numbers.append(n)
            final_i = 7 + 15 + final_i

        elif length_type_id == "1":
            total_number_of_subpackets = bin_to_dec(binary_transmission[7 : 7 + 11])
            for _ in range(total_number_of_subpackets):
                i, n = parse_packet(binary_transmission[7 + 11 + final_i :])
                final_i += i
                numbers.append(n)
            final_i = 7 + 11 + final_i

        if type_id == 0:
            n = sum(numbers)
        if type_id == 1:
            n = functools.reduce(lambda a, b: a * b, numbers)
        if type_id == 2:
            n = min(numbers)
        if type_id == 3:
            n = max(numbers)
        if type_id == 5:
            n = int(numbers[0] > numbers[1])
        if type_id == 6:
            n = int(numbers[0] < numbers[1])
        if type_id == 7:
            n = int(numbers[0] == numbers[1])
        return final_i, n


with open("input.txt") as f:
    transmission = f.readlines()[0].strip()
binary_transmission = hex_to_bin(transmission)
i, n = parse_packet(binary_transmission)

print("part1:", version_sum)
print("part2:", n)
