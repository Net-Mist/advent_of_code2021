import tqdm
from z3 import And, Distinct, Int, Or, Solver

# 000
# 1 2
# 333
# 4 5
# 666
#
number_to_seven_seg = [
    [0, 1, 2, 4, 5, 6],
    [2, 5],
    [0, 2, 3, 4, 6],
    [0, 2, 3, 5, 6],
    [1, 2, 3, 5],
    [0, 1, 3, 5, 6],
    [0, 1, 3, 4, 5, 6],
    [0, 2, 5],
    [0, 1, 2, 3, 4, 5, 6],
    [0, 1, 2, 3, 5, 6],
]


# the 13 input numbers
numbers = [Int(f"n_{i}") for i in range(14)]
numbers_condition = And(
    Distinct(numbers[:10]),
    *(And(n >= 0, n <= 9) for n in numbers),
)

# the displayed positions
seven_seg = [Int(f"s_{i}") for i in range(7)]
seven_seg_condition = And(
    Distinct(seven_seg),
    *(And(n >= 0, n <= 6) for n in seven_seg),
)


with open("input.txt") as f:
    lines = f.readlines()

question_1_counter = 0
question_2_number = 0
for i, line in tqdm.tqdm(enumerate(lines)):
    s = Solver()
    s.add(numbers_condition, seven_seg_condition)
    encoded_numbers = line.replace("|", "").split()
    for i, encoded_number in enumerate(encoded_numbers):
        new_conditions = []
        for j, n in enumerate(number_to_seven_seg):
            if len(n) != len(encoded_number):
                continue
            number_condition = numbers[i] == j
            signal_condition = And(
                [Or([seven_seg[ord(c) - ord("a")] == real_position for real_position in n]) for c in encoded_number]
            )
            new_conditions.append(And(number_condition, signal_condition))
        s.add(Or(new_conditions))
    s.check()

    out_n = []
    for i in range(4):
        n = s.model()[numbers[10 + i]].as_long()
        if n in [1, 4, 7, 8]:
            question_1_counter += 1
        out_n.append(n)
    question_2_number += sum(out_n[i] * 10 ** (3 - i) for i in range(4))

print("part1:", question_1_counter)
print("part2:", question_2_number)
