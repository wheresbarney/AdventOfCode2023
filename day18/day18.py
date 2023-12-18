# https://adventofcode.com/2023/day/18


from day16.day16 import DIR_OFFSETS


def q1(input):
    dug = set()
    current = (0, 0)
    for dir, length in [(t[0], int(t[1])) for t in [line.split() for line in input]]:
        offset = DIR_OFFSETS[dir]
        for _ in range(length):
            current = (current[0] + offset[0], current[1] + offset[1])
            dug.add(current)

    assert current == (0, 0), f"ended on {current}"

    minx, maxx = min([p[0] for p in dug]), max([p[0] for p in dug])
    miny, maxy = min([p[1] for p in dug]), max([p[1] for p in dug])

    outside = set()
    for y in (miny, maxy):
        for x in range(minx, maxx + 1):
            if (x, y) in dug or (x, y) in outside:
                continue
            outside |= expand_region((x, y), (minx, miny), (maxx, maxy), dug)

    for x in (minx, maxx):
        for y in range(miny, maxy + 1):
            if (x, y) in dug or (x, y) in outside:
                continue
            outside |= expand_region((x, y), (minx, miny), (maxx, maxy), dug)

    for y in range(miny, maxy + 1):
        print(
            " ".join(
                [
                    "#" if (x, y) in dug else "O" if (x, y) in outside else "."
                    for x in range(minx, maxx + 1)
                ]
            )
        )
    return (maxx - minx + 1) * (maxy - miny + 1) - len(outside)


def expand_region(point, topleft, bottomright, boundary):
    region = set()
    queue = [point]
    while queue:
        point = queue.pop()
        if (
            point[0] < topleft[0]
            or point[0] > bottomright[0]
            or point[1] < topleft[1]
            or point[1] > bottomright[1]
            or point in boundary
            or point in region
        ):
            continue

        region.add(point)
        queue += (
            (point[0] + 1, point[1]),
            (point[0] - 1, point[1]),
            (point[0], point[1] + 1),
            (point[0], point[1] - 1),
        )
    return region


def q2(input):
    current = (0, 0)
    vertices = []
    perimeter = 0

    OFFSETS = {"0": (1, 0), "1": (0, 1), "2": (-1, 0), "3": (0, -1)}
    for offset, length in [
        (OFFSETS[t[7]], int(t[2:7], 16)) for t in [line.split()[2] for line in input]
    ]:
        current = (current[0] + offset[0] * length, current[1] + offset[1] * length)
        perimeter += length
        vertices.append(current)

    assert current == (0, 0), f"ended on {current}"

    enclosed_area = shoelace(vertices)

    # Pick's Theorem: https://en.wikipedia.org/wiki/Pick%27s_theorem
    enclosed_points = enclosed_area + 1 - perimeter // 2
    return enclosed_points + perimeter


# Shoelace Theorem: https://en.wikipedia.org/w/index.php?title=Shoelace_formula&oldid=1190504759
def shoelace(vertices):
    return (
        abs(
            sum(
                [
                    vertices[i][0] * vertices[(i + 1) % len(vertices)][1]
                    - vertices[i][1] * vertices[(i + 1) % len(vertices)][0]
                    for i in range(len(vertices))
                ]
            )
        )
        // 2
    )
