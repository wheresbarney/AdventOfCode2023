# https://adventofcode.com/2023/day/11


def solve(input, expansion_factor):
    blank_rows = [r for r in range(len(input)) if "#" not in input[r]]
    blank_cols = [
        c
        for c in range(len(input[0]))
        if all([input[r][c] != "#" for r in range(len(input))])
    ]
    galaxies = [
        (c, r)
        for r in range(len(input))
        for c in range(len(input[0]))
        if input[r][c] == "#"
    ]

    total_dist = 0
    for i, galaxy in enumerate(galaxies):
        for j, other_galaxy in enumerate(galaxies[i + 1 :]):
            horiz = abs(galaxy[0] - other_galaxy[0])
            vert = abs(galaxy[1] - other_galaxy[1])
            horiz += (expansion_factor - 1) * len(
                [
                    c
                    for c in blank_cols
                    if c > min(galaxy[0], other_galaxy[0])
                    and c < max(galaxy[0], other_galaxy[0])
                ]
            )
            vert += (expansion_factor - 1) * len(
                [
                    r
                    for r in blank_rows
                    if r > min(galaxy[1], other_galaxy[1])
                    and r < max(galaxy[1], other_galaxy[1])
                ]
            )
            # print(
            #     f"expanded dist between galaxies {i+1} {galaxy} and {i+j+2} {other_galaxy}: "
            #     + f"{horiz+vert} {horiz=}, {vert=}"
            # )
            total_dist += horiz + vert
    return total_dist


def q1(input):
    return solve(input, 2)


def q2(input):
    return solve(input, 1_000_000)
