# https://adventofcode.com/2023/day/16


def q1(input):
    rays = trace((0, 0), "R", input, set())
    return len({ray[0] for ray in rays})


def q2(input):
    best = 0
    for i in range(len(input[0])):
        rays = trace((i, 0), "D", input, set())
        best = max(best, len({ray[0] for ray in rays}))

        rays = trace((i, len(input) - 1), "U", input, set())
        best = max(best, len({ray[0] for ray in rays}))

    for i in range(len(input)):
        rays = trace((0, i), "R", input, set())
        best = max(best, len({ray[0] for ray in rays}))

        rays = trace((len(input[0]) - 1, i), "L", input, set())
        best = max(best, len({ray[0] for ray in rays}))

    return best


DIR_OFFSETS = {"L": (-1, 0), "R": (1, 0), "U": (0, -1), "D": (0, 1)}
REFLECTIONS = {
    "\\": {"L": "U", "R": "D", "U": "L", "D": "R"},
    "/": {"L": "D", "R": "U", "U": "R", "D": "L"},
}


def trace(cell, dir, map, visited):
    if cell[0] < 0 or cell[0] >= len(map[0]) or cell[1] < 0 or cell[1] >= len(map):
        return visited

    if (cell, dir) in visited:
        return visited
    visited.add((cell, dir))

    def next_cell(cell, dir, map):
        offset = DIR_OFFSETS[dir]
        return (cell[0] + offset[0], cell[1] + offset[1]), dir, map

    symbol = map[cell[1]][cell[0]]

    if symbol == "-" and dir in "UD":
        return trace(*next_cell(cell, "L", map), visited) | trace(
            *next_cell(cell, "R", map), visited
        )

    if symbol == "|" and dir in "LR":
        return trace(*next_cell(cell, "U", map), visited) | trace(
            *next_cell(cell, "D", map), visited
        )

    if symbol in "\\/":
        return trace(*next_cell(cell, REFLECTIONS[symbol][dir], map), visited)

    # fast-forward to edge or next mirror/splitter
    # to avoid stack overflow through too much recursion
    while True:
        cell, _, _ = next_cell(cell, dir, map)
        if cell[0] < 0 or cell[0] >= len(map[0]) or cell[1] < 0 or cell[1] >= len(map):
            return visited
        symbol = map[cell[1]][cell[0]]
        if symbol == ".":
            visited.add((cell, dir))
        else:
            return trace(cell, dir, map, visited)
