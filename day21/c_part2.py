from collections import Counter, defaultdict

# map for every set (score_player1, score_player2, position_player1, position_player2) the number of universe
scores_and_position = {(0, 0, 6, 3): 1}
player = 0
n_wins = [0, 0]


def roll_dice_3() -> list:
    possible_scores = [0]
    for _ in range(3):
        new_possible_scores = []
        for s in possible_scores:
            for j in range(3):
                new_possible_scores.append(s + j + 1)
        possible_scores = new_possible_scores
    return possible_scores


one_turn_dice = Counter(roll_dice_3())

while scores_and_position:
    new_scores_and_position = defaultdict(lambda: 0)
    for k, v in scores_and_position.items():
        for dice, time in one_turn_dice.items():
            scores = [k[0], k[1]]
            positions = [k[2], k[3]]

            positions[player] = (positions[player] + dice - 1) % 10 + 1
            scores[player] = scores[player] + positions[player]

            if scores[player] >= 21:
                n_wins[player] += v * time
            else:
                new_scores_and_position[(scores[0], scores[1], positions[0], positions[1])] += v * time
    scores_and_position = new_scores_and_position
    player = 1 - player

print(max(n_wins))
