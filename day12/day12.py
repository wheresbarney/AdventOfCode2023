# https://adventofcode.com/2023/day/12


import functools


def q1(input):
    combos = []
    for pattern, groups in parse(input):
        print(f"Counting perms for {pattern}, {groups}...")
        combos.append(
            Node(pattern, groups).count_matching(
                lambda node: (not node.children) and valid(node.pattern, groups)
            )
        )

    return sum(combos)


def q2(input):
    combos = []
    for pattern, groups in parse(input):
        pattern = "?".join((pattern,) * 5)
        groups = tuple(groups * 5)
        combos.append(num_perms(pattern, groups, False))

    return sum(combos)


@functools.lru_cache
def num_perms(pattern, groups, in_group):
    def decr(groups):
        return (groups[0] - 1,) + groups[1:]

    if not groups:
        return 0 if "#" in pattern else 1
    if not pattern:
        return 0 if sum(groups) else 1
    if groups[0] == 0:
        return (
            num_perms(pattern[1:], groups[1:], False) if pattern[0] in {"?", "."} else 0
        )
    if in_group:
        return (
            num_perms(pattern[1:], decr(groups), True)
            if pattern[0] in {"?", "#"}
            else 0
        )
    if pattern[0] == "#":
        return num_perms(pattern[1:], decr(groups), True)
    if pattern[0] == ".":
        return num_perms(pattern[1:], groups, False)
    assert pattern[0] == "?", "Unexpected pattern " + pattern
    return num_perms(pattern[1:], groups, False) + num_perms(
        pattern[1:], decr(groups), True
    )


def parse(input):
    patterns_and_groups = []
    for pattern, groups in [line.split() for line in input]:
        groups = [int(n) for n in groups.split(",")]
        patterns_and_groups.append((pattern, groups))
    return patterns_and_groups


def valid(pattern, groups):
    assert "?" not in pattern, "Unexpected ? in " + pattern
    return [len(c) for c in pattern.replace(".", " ").split()] == groups


class Node:
    def __init__(self, pattern, groups):
        self.pattern = None
        self.children = {}
        if "?" in pattern:
            self.children = {
                Node(d, groups) for d in [pattern.replace("?", s, 1) for s in ".#"]
            }
        else:
            self.pattern = pattern

    def count_matching(self, predicate):
        total = 1 if predicate(self) else 0
        for child in self.children:
            total += child.count_matching(predicate)

        return total
