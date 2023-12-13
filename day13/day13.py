# https://adventofcode.com/2023/day/13


def parse(input):
    patterns = []
    current_pattern = []
    for line in input:
        if line:
            current_pattern.append(line)
        else:
            patterns.append(current_pattern)
            current_pattern = []
    patterns.append(current_pattern)
    return patterns


def q1(input):
    horiz = []
    vert = []
    for pattern in parse(input):
        horiz.append(rows_above_horiz_axis(pattern))

    for pattern in parse(input):
        # transpose, repeat
        vert.append(rows_above_horiz_axis(list(zip(*pattern))))

    return sum(horiz) * 100 + sum(vert)


def rows_above_horiz_axis(pattern):
    for candidate in range(1, len(pattern)):
        symmetric = True
        for offset in range(min(candidate, len(pattern) - candidate)):
            if pattern[candidate - offset - 1] != pattern[candidate + offset]:
                symmetric = False
                break
        if symmetric:
            # print(f"Found horiz symmetry after {candidate} rows in")
            # [print(r) for r in pattern]
            return candidate
    return 0


def q2(input):
    horiz = []
    vert = []
    for pattern in parse(input):
        horiz.append(rows_above_horiz_axis_with_smudge(pattern))

    for pattern in parse(input):
        # transpose, repeat
        vert.append(rows_above_horiz_axis_with_smudge(list(zip(*pattern))))

    return sum(horiz) * 100 + sum(vert)


def rows_above_horiz_axis_with_smudge(pattern):
    for candidate in range(1, len(pattern)):
        symmetric = True
        fixed_smudge = False
        for offset in range(min(candidate, len(pattern) - candidate)):
            if pattern[candidate - offset - 1] != pattern[candidate + offset]:
                if (
                    not fixed_smudge
                    and len(
                        [
                            p
                            for p in zip(
                                pattern[candidate - offset - 1],
                                pattern[candidate + offset],
                            )
                            if p[0] != p[1]
                        ]
                    )
                    == 1
                ):
                    fixed_smudge = True
                else:
                    symmetric = False
                    break
        if symmetric and fixed_smudge:
            # print(f"Found horiz symmetry after {candidate} rows in")
            # [print(r) for r in pattern]
            return candidate
    return 0
