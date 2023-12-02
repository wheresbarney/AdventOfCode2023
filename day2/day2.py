# https://adventofcode.com/2023/day/2

from math import prod

def parse_dice(dice):
  count, colour = dice.split(' ')
  return int(count), colour


def parse(input):
    games = []
    for line in input:
        glimpses = [glimpse.split(', ') for glimpse in line.split(': ')[1].split('; ')]
        games.append([[parse_dice(dice) for dice in glimpse] for glimpse in glimpses])
    return games


def q1(lines):
    games = parse(lines)
    total = 0
    limits = {'red': 12, 'green': 13, 'blue': 14}
    for i, game in enumerate(games):
        if not [colour for t in game for count, colour in t if count > limits[colour]]:
            total += i + 1
    return total


def q2(lines):
    total = 0
    for game in parse(lines):
        colours = ({t[1] for a in game for t in a})
        total += prod([max([t[0] for a in game for t in a if t[1] == colour]) for colour in colours])
    return total
