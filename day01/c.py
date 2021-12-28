with open("input.txt") as f:
    inputs = [int(line.strip()) for line in f.readlines()]


increase = 0
for i in range(len(inputs) - 1):
    a = inputs[i]
    b = inputs[i + 1]
    if a < b:
        increase += 1

print("part 1:", increase)


increase = 0
for i in range(len(inputs) - 3):
    a = inputs[i] + inputs[i + 1] + inputs[i + 2]
    b = inputs[i + 1] + inputs[i + 2] + inputs[i + 3]
    if a < b:
        increase += 1

print("part 2:", increase)
