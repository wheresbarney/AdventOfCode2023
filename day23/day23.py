# https://adventofcode.com/2023/day/23

from heapq import heappop, heappush
from sys import maxsize
from collections import defaultdict
from math import inf


def q1(input):
    start = (input[0].index("."), 0)
    end = (input[-1].index("."), len(input) - 1)
    return dijkstra_longest_path(start, end, input, True)


def q2(input):
    start = (input[0].index("."), 0)
    end = (input[-1].index("."), len(input) - 1)

    map = compress_map(start, end, input)
    return max(dfs(start, end, 0, map, {start}))
    # return dijkstra_longest_path(start, end, input, False)


def dfs(pos, end, distance, graph, seen):
    if pos == end:
        yield distance

    for next_node, step_length in graph[pos]:
        if next_node in seen:
            continue
        yield from dfs(
            next_node, end, distance + step_length, graph, seen | {next_node}
        )


def compress_map(
    start: tuple[int, int], end: tuple[int, int], input: list[str]
) -> dict[tuple[int, int], list[tuple[tuple[int, int], int]]]:
    def valid_paths(pos: tuple[int, int], map: list[str]) -> list[tuple[int, int]]:
        neighbours = [
            (pos[0] + 1, pos[1]),
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1),
        ]
        return [
            (x, y)
            for x, y in neighbours
            if 0 <= x < len(map[0]) and 0 <= y < len(map) and map[y][x] != "#"
        ]

    crossroads = (
        [start]
        + [
            (x, y)
            for y in range(len(input))
            for x in range(len(input[0]))
            if len(valid_paths((x, y), input)) > 2
        ]
        + [end]
    )

    graph = defaultdict(list)
    for crossroad in crossroads:
        for neighbour in valid_paths(crossroad, input):
            previous, current = crossroad, neighbour
            distance = 1
            while current not in crossroads:
                previous, current = (
                    current,
                    [
                        neighbour
                        for neighbour in valid_paths(current, input)
                        if neighbour != previous
                    ][0],
                )
                distance += 1
            graph[crossroad].append((current, distance))

    return graph


DIR_OFFSETS = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}
ABSURDLY_LONG_PATH = maxsize


def dijkstra_longest_path(start, end, map, slopes_icy):
    def sort_key(distance: int) -> int:
        return ABSURDLY_LONG_PATH - distance

    distances = {}
    queue: list[tuple[int, tuple[int, int], set[tuple[int, int]]]] = [
        (sort_key(0), start, {start})
    ]
    while queue:
        dist_key, node, visited = heappop(queue)
        dist = sort_key(dist_key)
        for symbol, turn in DIR_OFFSETS.items():
            x, y = node[0] + turn[0], node[1] + turn[1]
            if 0 <= x < len(map[0]) and 0 <= y < len(map):
                terrain = map[y][x]
                if terrain == "#" or (
                    slopes_icy and terrain != symbol and terrain != "."
                ):
                    continue
                new_pos = (x, y)
                if new_pos in visited:
                    continue
                if not path_exists(new_pos, end, map, visited):
                    continue
                new_dist = dist + 1
                if new_dist > distances.get(new_pos, 0):
                    distances[new_pos] = new_dist
                heappush(queue, (sort_key(new_dist), new_pos, visited | {new_pos}))

    return distances[end]


def path_exists(start, to, map, forbidden):
    distances = defaultdict(lambda: inf)
    distances[start] = 0
    queue: list[tuple[int, tuple[int, int]]] = [(0, start)]
    while queue:
        dist, node = heappop(queue)
        if dist > distances[(node, dir)]:
            continue

        if node == to:
            return True

        for turn in DIR_OFFSETS.values():
            x, y = node[0] + turn[0], node[1] + turn[1]
            if (
                0 <= x < len(map[0])
                and 0 <= y < len(map)
                and map[y][x] != "#"
                and (x, y) not in forbidden
            ):
                new_pos = (x, y)
                new_dist = dist + 1
                if new_dist < distances[new_pos]:
                    distances[new_pos] = new_dist
                    heappush(queue, (new_dist, new_pos))
    return False
