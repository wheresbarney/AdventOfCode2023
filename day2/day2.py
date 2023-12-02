# https://adventofcode.com/2023/day/2

from math import prod as product

def parse(input):
    games = []
    for line in input:
        game = []
        glimpses = line.split(': ')[1].split('; ')
        for glimpse_str in glimpses:
            glimpse = []
            for count_and_colours in glimpse_str.split(', '):
                count, colour = count_and_colours.split(' ')
                glimpse.append((int(count), colour))
            game.append(glimpse)
        games.append(game)
    return games


def q1(lines):
    games = parse(lines)
    limits = {'red': 12, 'green': 13, 'blue': 14}
    total = 0
    for i, game in enumerate(games):
        valid = True
        for glimpse in game:
            over_limit = any([count > limits[colour] for count, colour in glimpse])
            if over_limit:
                valid = False
                break
        if valid:
            total += i + 1
    return total


def q2(lines):
    total = 0
    for game in parse(lines):
        colour_totals = {}
        for glimpse in game:
            for count, colour in glimpse:
                if colour_totals.get(colour, 0) < count:
                    colour_totals[colour] = count
        total += product(colour_totals.values())
    return total
