from z3 import And, ArithRef, Int, IntNumRef, IntVal, Solver, sat, simplify, unsat

with open("input.txt") as f:
    lines = f.readlines()


numbers = [Int(f"x{i}") for i in range(14)]
numbers_c = [And(numbers[i] >= 1, numbers[i] <= 9) for i in range(14)]
s = Solver()
s.add(numbers_c)
alu_state = {
    "w": IntVal(0),
    "x": IntVal(0),
    "y": IntVal(0),
    "z": IntVal(0),
}

input_cursor = 0
for i, line in enumerate(lines):
    for k in alu_state.keys():
        # simplify expression and create intermediate solver
        if type(alu_state[k]) not in [int]:
            alu_state[k] = simplify(alu_state[k])
        if type(alu_state[k]) not in [IntNumRef, ArithRef, int] and i < 200:
            s.push()
            s.add(And(alu_state[k]))
            if s.check() == unsat:
                print(alu_state[k], "is always false")
                alu_state[k] = IntVal(0)
            s.pop()
    print("line", i + 1, ":", line[:-1])

    words = line.split()

    if words[0] == "inp":
        alu_state[words[1]] = numbers[input_cursor]
        input_cursor += 1
        continue

    rt = alu_state[words[2]] if words[2] in alu_state else int(words[2])
    if words[0] == "mul":
        n = alu_state[words[1]] * rt
    if words[0] == "add":
        n = alu_state[words[1]] + rt
    if words[0] == "mod":
        n = alu_state[words[1]] % rt
    if words[0] == "div":
        if type(alu_state[words[1]]) == int:
            n = alu_state[words[1]] // rt
        else:
            n = alu_state[words[1]] / IntVal(rt)
    if words[0] == "eql":
        if rt == 0:
            rt = False
        if rt == 1:
            rt = True
        n = alu_state[words[1]] == rt
    alu_state[words[1]] = n

s.add(And(alu_state["z"] == 0))

# question 1

push_counter = 0

for i in range(14):
    while s.check() == sat:
        m = s.model()
        for n in numbers:
            print(m[n], end="")
        print()

        s.push()
        push_counter += 1
        new_condition = numbers[i] > m[numbers[i]]
        s.add(new_condition)
    # replace last condition with a less strict one
    new_condition = numbers[i] >= m[numbers[i]]
    s.pop()
    push_counter -= 1
    s.add(And(new_condition))

m = s.model()
print("part1:", end=" ")
for n in numbers:
    print(m[n], end="")
print()


# question 2
for _ in range(push_counter):
    s.pop()


for i in range(14):
    while s.check() == sat:
        m = s.model()
        for n in numbers:
            print(m[n], end="")
        print()

        s.push()
        new_condition = numbers[i] < m[numbers[i]]
        s.add(And(new_condition))
    # replace last condition with a less strict one
    new_condition = numbers[i] <= m[numbers[i]]
    s.pop()
    s.add(And(new_condition))


m = s.model()
print("part2:", end=" ")
for n in numbers:
    print(m[n], end="")
print()
