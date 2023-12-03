# https://adventofcode.com/2023/day/3


def parse(lines):
    part_nums = []
    symbols = []
    for line_num, line in enumerate(lines):
        current_num = ""
        for pos, char in enumerate(line):
            if char.isdigit():
                current_num += char
            else:
                if current_num:
                    part_nums.append(
                        (
                            line_num,
                            pos - len(current_num),
                            pos - 1,
                            int(current_num),
                        )
                    )
                    current_num = ""
                if char != "." and not char.isdigit():
                    symbols.append((line_num, pos, char))
        if current_num:  # EOL also terminates number
            part_nums.append(
                (line_num, pos - len(current_num), pos - 1, int(current_num))
            )
    # print(f"{part_nums=}")
    # print(f"{symbols=}")
    return part_nums, symbols


def q1(lines):
    part_nums, symbols = parse(lines)
    total = 0

    for pline, pstart, pend, part_num in part_nums:
        for sline, spos, _ in symbols:
            if (
                sline >= pline - 1
                and sline <= pline + 1
                and spos >= pstart - 1
                and spos <= pend + 1
            ):
                total += part_num
                break
            if sline > pline + 1:
                break  # lines and symbols ordered by line, no need to continue
    return total


def q2(lines):
    part_nums, symbols = parse(lines)
    total = 0

    for sline, spos, symbol in symbols:
        if symbol != "*":
            continue
        adjacent_parts = []
        for pline, pstart, pend, part_num in part_nums:
            if (
                sline >= pline - 1
                and sline <= pline + 1
                and spos >= pstart - 1
                and spos <= pend + 1
            ):
                adjacent_parts.append(part_num)

            if pline > sline + 1:
                break  # lines and symbols ordered by line, no need to continue

        if len(adjacent_parts) == 2:
            # print(f"found gear at ({sline},{spos}) => {adjacent_parts}")
            total += adjacent_parts[0] * adjacent_parts[1]

    return total
