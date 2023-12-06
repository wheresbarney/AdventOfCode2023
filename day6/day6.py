# https://adventofcode.com/2023/day/6


from math import prod


def parse(lines):
    lines = [[int(n) for n in line.split(":")[1].split()] for line in lines]
    return zip(lines[0], lines[1])


def q1(input):
    races = parse(input)
    ways_to_win_all = []
    for time, distance in races:
        ways_to_win = 0
        for charge_time in range(1, time):  # no point charging for 0 or max ms
            if charge_time * (time - charge_time) > distance:
                ways_to_win += 1
        ways_to_win_all.append(ways_to_win)
    return prod(ways_to_win_all)


def q2(input):
    time, dist = [int("".join(line.split(":")[1].split())) for line in input]

    ways_to_win = 0
    for charge_time in range(1, time):  # no point charging for 0 or max ms
        if charge_time * (time - charge_time) > dist:
            ways_to_win += 1
        elif ways_to_win > 0:
            break  # remaining range will all lose race, no point
    return ways_to_win
