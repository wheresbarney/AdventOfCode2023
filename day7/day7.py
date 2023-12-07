# https://adventofcode.com/2023/day/7


from collections import Counter


FACE_VAL = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
FACE_VAL.update({str(d): d for d in range(2, 10)})


def pattern(cards):
    counts = [c[1] for c in Counter(cards).most_common()]
    if counts[0] == 5:
        return 7
    if counts[0] == 4:
        return 6
    if counts[0] == 3:
        if counts[1] == 2:
            return 5
        return 4
    if counts[0] == 2:
        if counts[1] == 2:
            return 3
        return 2
    return 1


def q1(lines):
    hands = sorted(
        [(hand[0], int(hand[1])) for hand in [line.split() for line in lines]],
        key=lambda hand: tuple([pattern(hand[0])] + [FACE_VAL.get(c) for c in hand[0]]),
    )
    return sum([(i + 1) * hand[1] for i, hand in enumerate(hands)])


def pattern_with_wildcard(cards):
    counter = Counter(cards)
    most_common = counter.most_common()
    counts = [c[1] for c in most_common]

    firsts = counts[0]
    seconds = counts[1] if len(counts) > 1 else 0
    jokers = counter["J"]

    if most_common[0][0] == "J" or (jokers >= 1 and most_common[1][0] == "J"):
        # jokers in first or second place, merge them into firsts and recalculate seconds
        firsts += seconds
        seconds = 0 if len(counts) <= 2 else counts[2]
    elif jokers > 0:
        # jokers, but not in first/second place
        # just add to firsts
        firsts += jokers

    if firsts == 5:
        return 7
    if firsts == 4:
        return 6
    if firsts == 3:
        if seconds == 2:
            return 5
        return 4
    if firsts == 2:
        if seconds == 2:
            return 3
        return 2
    return 1


def q2(lines):
    FACE_VAL["J"] = 1
    hands = sorted(
        [(hand[0], int(hand[1])) for hand in [line.split() for line in lines]],
        key=lambda hand: tuple(
            [pattern_with_wildcard(hand[0])] + [FACE_VAL.get(c) for c in hand[0]]
        ),
    )
    return sum([(i + 1) * hand[1] for i, hand in enumerate(hands)])
