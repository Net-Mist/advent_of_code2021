import re

with open("input.txt") as f:
    lines = f.readlines()

cmds = []
for line in lines:
    m = re.match(r"(-?\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line)
    cmds.append((m.groups()[0],) + tuple(int(i) for i in m.groups()[1:]))


def intersect_and_split(known_zones: list[tuple], new_zone: tuple) -> int:
    for z, zone in enumerate(known_zones):
        if (
            zone[0] > new_zone[1]
            or zone[1] < new_zone[0]
            or zone[2] > new_zone[3]
            or zone[3] < new_zone[2]
            or zone[4] > new_zone[5]
            or zone[5] < new_zone[4]
        ):
            continue  # in this case, no intersections
        else:
            split = [[], [], []]
            keep = [[], [], []]
            for i in range(3):
                if (
                    new_zone[0 + 2 * i] < zone[0 + 2 * i] < new_zone[1 + 2 * i]
                    and new_zone[0 + 2 * i] < zone[1 + 2 * i] < new_zone[1 + 2 * i]
                ):
                    # then zone is full inside new_zone : split new_zone into 3
                    split[i] = [
                        [new_zone[0 + 2 * i], zone[0 + 2 * i] - 1],
                        [zone[0 + 2 * i], zone[1 + 2 * i]],
                        [zone[1 + 2 * i] + 1, new_zone[1 + 2 * i]],
                    ]
                    keep[i] = [True, False, True]
                elif new_zone[0 + 2 * i] < zone[0 + 2 * i] <= new_zone[1 + 2 * i]:
                    split[i] = [[new_zone[0 + 2 * i], zone[0 + 2 * i] - 1], [zone[0 + 2 * i], new_zone[1 + 2 * i]]]
                    keep[i] = [True, False]
                elif new_zone[0 + 2 * i] <= zone[1 + 2 * i] < new_zone[1 + 2 * i]:
                    split[i] = [[new_zone[0 + 2 * i], zone[1 + 2 * i]], [zone[1 + 2 * i] + 1, new_zone[1 + 2 * i]]]
                    keep[i] = [False, True]
                else:
                    split[i] = [[new_zone[0 + 2 * i], new_zone[1 + 2 * i]]]
                    keep[i] = [False]

            # cut up to 9 zones
            new_zones = []
            for i, keep_x in enumerate(keep[0]):
                for j, keep_y in enumerate(keep[1]):
                    for k, keep_z in enumerate(keep[2]):
                        if keep_x + keep_y + keep_z:
                            new_zones.append(
                                (
                                    split[0][i][0],
                                    split[0][i][1],
                                    split[1][j][0],
                                    split[1][j][1],
                                    split[2][k][0],
                                    split[2][k][1],
                                )
                            )
            s = 0
            for zone in new_zones:
                s += intersect_and_split(known_zones[z + 1 :], zone)

            return s
    return (new_zone[1] - new_zone[0] + 1) * (new_zone[3] - new_zone[2] + 1) * (new_zone[5] - new_zone[4] + 1)


n_on = 0
zones = []
for cmd in cmds[::-1]:
    if cmd[0] == "on":
        n_on += intersect_and_split(zones, cmd[1:])
    zones.append(cmd[1:])
print(n_on)
