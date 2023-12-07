# https://adventofcode.com/2023/day/7


from collections import Counter


FACE_VALS = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
FACE_VALS.update({str(d): d for d in range(2, 10)})


def parse_and_sort(lines, key):
    hands = [(hand[0], int(hand[1])) for hand in [line.split() for line in lines]]
    return sum([(i + 1) * hand[1] for i, hand in enumerate(sorted(hands, key=key))])


def hand_score(firsts, seconds):
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


def score_hand(cards):
    counts = [c[1] for c in Counter(cards).most_common()]
    firsts = counts[0]
    seconds = counts[1] if len(counts) > 1 else 0
    return hand_score(firsts, seconds)


def score_hand_with_jokers(cards):
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

    return hand_score(firsts, seconds)


def q1(lines):
    return parse_and_sort(
        lines,
        lambda hand: tuple([score_hand(hand[0])] + [FACE_VALS.get(c) for c in hand[0]]),
    )


def q2(lines):
    FACE_VALS["J"] = 1
    return parse_and_sort(
        lines,
        lambda hand: tuple(
            [score_hand_with_jokers(hand[0])] + [FACE_VALS.get(c) for c in hand[0]]
        ),
    )
