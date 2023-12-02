# https://adventofcode.com/2023/day/1


def q1(lines):
    sum = 0
    for line in lines:
        digits = [c for c in line if c.isdecimal()]
        sum += int(digits[0] + digits[-1])
    return sum


def q2(lines):
    sum = 0
    for line in lines:
        first = last = None
        for i in range(len(line)):
            if signal := extract_signal(line[i:]):
                last = signal
                if not first:
                    first = last
        sum += int(str(first) + str(last))
    return sum


WORDS_TO_NUMS = {
    s: i + 1
    for i, s in enumerate(
        ["one", "two", "three", "four", "five",
            "six", "seven", "eight", "nine"]
    )
}


def extract_signal(s):
    if s[0].isdecimal():
        return int(s[0])
    for w, n in WORDS_TO_NUMS.items():
        if s[: len(w)] == w:
            return n

    return None
