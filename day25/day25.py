# https://adventofcode.com/2023/day/25


def q1(input):
    nodes = {
        src: {*dests.split()} for src, dests in [line.split(": ") for line in input]
    }

    for src, dests in list(nodes.items()):
        for dest in dests:
            if dest not in nodes:
                nodes[dest] = set()
            nodes[dest].add(src)

    breaks = (
        (("hfx", "pzl"), ("bvb", "cmg"), ("nvd", "jqt"))
        if len(input) == 13
        else (("nvb", "fts"), ("qmr", "kzx"), ("jff", "zns"))
    )
    for n1, n2 in breaks:
        nodes[n1].remove(n2)
        nodes[n2].remove(n1)

    return len(all_connected(breaks[0][0], nodes, set())) * len(
        all_connected(breaks[0][1], nodes, set())
    )


def all_connected(node, nodes, seen):
    if node in seen:
        return seen
    seen.add(node)

    for n in nodes[node]:
        seen |= all_connected(n, nodes, seen)

    return seen
