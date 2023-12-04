# https://adventofcode.com/2023/day/4


def parse(lines):
    return [
        [{int(n) for n in card.split()} for card in line.split(":")[1].split("|")]
        for line in lines
    ]


def q1(lines):
    total = 0
    for card in parse(lines):
        common = len(card[0] & card[1])
        if common:
            total += 2 ** (common - 1)
    return total


def q2(lines):
    master_cards = parse(lines)
    card_counts = [1] * len(master_cards)
    for i, card in enumerate(master_cards):
        common = len(card[0] & card[1])
        for n in range(i + 1, min(i + 1 + common, len(master_cards))):
            card_counts[n] += card_counts[i]
    return sum(card_counts)
