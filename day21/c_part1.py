scores = [0, 0]
positions = [6, 3]
player = 0
dice = 1

n_roll = 0


def roll_dice(dice: int) -> tuple[int, int]:
    s = 0
    for _ in range(3):
        s += dice
        dice += 1
        if dice > 100:
            dice = 1
    return dice, s


while True:
    dice, dice_sum = roll_dice(dice)
    n_roll += 3
    positions[player] = (positions[player] + dice_sum - 1) % 10 + 1
    scores[player] += positions[player]
    if scores[player] >= 1000:
        break
    player = 1 - player

print(n_roll * scores[1 - player])
