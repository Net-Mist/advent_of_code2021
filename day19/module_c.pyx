cdef list _rotate_x(list points):
    new_test_sets = []
    new_test_sets.append(points)
    for _ in range(3):
        new_points = [(point[0], point[2], -point[1]) for point in points]
        new_test_sets.append(new_points)
        points = new_points
    return new_test_sets


cpdef list get_all_rotation(list points):
    all_point_rotations = []
    all_point_rotations += _rotate_x(points)

    # transform x to y 3 times
    for i in range(3):
        points = [(-point[1], point[0], point[2]) for point in points]
        all_point_rotations += _rotate_x(points)

    # transform x to z
    points = [(-point[2], point[1], point[0]) for point in points]
    all_point_rotations += _rotate_x(points)

    # transform z to -z
    points = [(-point[0], point[1], -point[2]) for point in points]
    all_point_rotations += _rotate_x(points)
    return all_point_rotations


def try_align(list s1, list s2):
    # for every possible angle (24)
    cdef int i
    cdef list s2b, intersect_points
    cdef tuple p1, p2, vect12, p, p_in_r2
    cdef char correct
    for i, s2b in enumerate(get_all_rotation(s2)):
        # randomly select 2 points and align on them (26**2)
        for p1 in s1:
            for p2 in s2b:
                # compute the position of scanner 2 compare to scanner 1
                vect12 = tuple(p1[i] - p2[i] for i in range(3))

                # compute the interesting points in both set
                intersect_points = []
                for p in s1:
                    if sum(abs(vect12[i] - p[i]) <= 1000 for i in range(3)) == 3:
                        intersect_points.append(p)

                if len(intersect_points) < 12:
                    continue

                # check if these points align well
                correct = True
                for p in intersect_points:
                    p_in_r2 = tuple(p[i] - vect12[i] for i in range(3))
                    if p_in_r2 not in s2b:
                        correct = False
                        break

                if not correct:
                    continue

                return True, i, vect12
    return False, 0, None
