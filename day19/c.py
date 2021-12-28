from module_c import get_all_rotation, try_align


def get_scanner_points(file: str) -> list[list[tuple[int, int, int]]]:
    with open(file) as f:
        lines = f.readlines()

    scanner_points = []
    points = []
    for line in lines:
        if line.startswith("---"):
            points = []
        elif "," in line:
            points.append(tuple(int(c) for c in line[:-1].split(",")))
        else:
            scanner_points.append(points)
    scanner_points.append(points)
    return scanner_points


def project(transform_r1r2: list, points: list) -> list:
    points = get_all_rotation(points)[transform_r1r2[0]]
    r = []
    for p in points:
        r.append(tuple(p[i] + transform_r1r2[1][i] for i in range(3)))
    return r


transform_r1r2 = {}  # give the transformation to from one ref to the other using angle and vect


scanner_points = get_scanner_points("input.txt")
all_points_r_0 = scanner_points[0].copy()

for i1, s1 in enumerate(scanner_points):
    for i2, s2 in enumerate(scanner_points):
        if i2 == i1:
            continue
        align, angle, vect = try_align(s1, s2)
        if align:
            print("scanner", i1, "and", i2, "aligned with angle", angle, "and vector", vect)
            transform_r1r2[(i1, i2)] = (angle, vect)

# compute distance to 0
distances = [-1] * len(scanner_points)
distances[0] = 0

while -1 in distances:
    for k in transform_r1r2.keys():
        if distances[k[0]] != -1 and distances[k[1]] == -1:
            distances[k[1]] = distances[k[0]] + 1
        if distances[k[1]] != -1 and distances[k[0]] == -1:
            distances[k[0]] = distances[k[1]] + 1


def project_r0(scanner_points: list) -> None:
    # project everything to R0
    for distance in range(max(distances), 0, -1):
        for j, d in enumerate(distances):
            if d != distance:
                continue
            # find a space nearer to 0
            for k, d in enumerate(distances):
                if d == distance - 1 and (k, j) in transform_r1r2.keys():
                    break
            print("project", j, "to", k)
            scanner_points[k] += project(transform_r1r2[(k, j)], scanner_points[j])


project_r0(scanner_points)
print("part1:", len(set(scanner_points[0])))


# part 2
new_scanner_points = []
for _ in range(len(scanner_points)):
    new_scanner_points.append([(0, 0, 0)])
scanner_points = new_scanner_points

project_r0(scanner_points)

distance = 0
for p1 in scanner_points[0]:
    for p2 in scanner_points[0]:
        distance = max(sum(abs(p1[i] - p2[i]) for i in range(3)), distance)
print("part2:", distance)
