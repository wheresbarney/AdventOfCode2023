# https://adventofcode.com/2023/day/14


from functools import lru_cache


def q1(input):
    rounds, squares = parse(input)

    total_load = 0
    for col in range(len(input[0])):
        col_rounds = sorted([r[1] for r in rounds if r[0] == col])
        col_squares = sorted([s[1] for s in squares if s[0] == col])
        next_free = 0
        while col_rounds:
            if not col_squares or col_rounds[0] < col_squares[0]:
                # print(f"col {col}: round rolled to slot {next_free+1}")
                total_load += len(input) - next_free
                next_free += 1
                col_rounds.pop(0)
            else:
                next_free = col_squares.pop(0) + 1
    return total_load


def q2_text_based(input):
    @lru_cache
    def rotate_clockwise(input):
        return tuple(["".join(reversed(t)) for t in zip(*input)])

    @lru_cache
    def tilt_right(input):
        return tuple(
            ["#".join(["".join(sorted(s)) for s in line.split("#")]) for line in input]
        )

    input = tuple(input)

    seen_layouts = {}
    for cycle in range(1, 1_000_000_001):
        for subcycle in range(4):
            input = rotate_clockwise(input)
            input = tilt_right(input)

        # print()
        # [print(line) for line in input]

        if input not in seen_layouts:
            seen_layouts[input] = cycle
        else:
            # loop detected
            loop_start = seen_layouts[input]
            loop_length = cycle - loop_start
            fast_fwd = (1_000_000_000 - loop_start) % loop_length + loop_start
            for layout, seen_at in seen_layouts.items():
                if seen_at == fast_fwd:
                    return sum(
                        [l.count("O") * (n + 1) for n, l in enumerate(reversed(layout))]
                    )

    return sum([l.count("O") * (n + 1) for n, l in enumerate(reversed(input))])


def q2(input):
    rounds, squares = parse(input)
    input = tuple(input)
    seen_rounds = {}
    for cycle in range(1, 1_000_000_001):
        for subcycle in range(4):
            rounds = compress(rounds, squares, input, subcycle)
        if rounds not in seen_rounds:
            seen_rounds[rounds] = cycle
        else:
            # loop detected
            loop_start = seen_rounds[rounds]
            loop_length = cycle - loop_start
            fast_fwd = (1_000_000_000 - loop_start) % loop_length + loop_start
            for seen_rounds, seen_at in seen_rounds.items():
                if seen_at == fast_fwd:
                    weight = 0
                    for r in range(len(input[0])):
                        weight += (len(input[0]) - r) * len(
                            [x for x, y in seen_rounds if y == r]
                        )
                    return weight

            # if cycle % 4 == 3:
            #     print(f"{cycle}: ⭥={cycle % 2 == 0} ↔={cycle % 4 >= 2}")
            #     for r in range(len(input)):
            #         col = ""
            #         for c in range(len(input[0])):
            #             p = (c, r)
            #             col += "O" if p in rounds else "#" if p in squares else "."
            #         print(col)
    weight = 0
    for r in range(len(input[0])):
        weight += (len(input[0]) - r) * len([x for x, y in rounds if y == r])
    return weight


def compress(rounds, squares, input, direction):
    if direction == 0:  # north
        descending = False
        northsouth = True
    elif direction == 1:  # west
        descending = False
        northsouth = False
    elif direction == 2:  # south
        descending = True
        northsouth = True
    else:  # east
        descending = True
        northsouth = False

    col_index = 0 if northsouth else 1
    row_index = 1 if northsouth else 0
    col_len = len(input[0]) if northsouth else len(input)
    next_free_seed = col_len - 1 if descending else 0
    next_free_bump = -1 if descending else 1

    def cmp(x, y):
        return (x > y) if descending else (x < y)

    new_rounds = []

    for col in range(col_len):
        current_rounds = sorted(
            [r[row_index] for r in rounds if r[col_index] == col], reverse=descending
        )
        col_squares = sorted(
            [s[row_index] for s in squares if s[col_index] == col], reverse=descending
        )
        next_free = next_free_seed
        while current_rounds:
            if not col_squares or cmp(current_rounds[0], col_squares[0]):
                new_rounds.append((col, next_free) if northsouth else (next_free, col))
                next_free += next_free_bump
                current_rounds.pop(0)
            else:
                next_free = col_squares.pop(0) + next_free_bump
    return tuple(new_rounds)


def parse(input):
    rounds = [
        (x, y)
        for y in range(len(input))
        for x in range(len(input[0]))
        if input[y][x] == "O"
    ]

    squares = [
        (x, y)
        for y in range(len(input))
        for x in range(len(input[0]))
        if input[y][x] == "#"
    ]
    return tuple(rounds), tuple(squares)
