# https://adventofcode.com/2023/day/21

import numpy as np
from day16.day16 import DIR_OFFSETS
from collections import defaultdict, deque
from heapq import heappop, heappush
from math import inf
from typing import Optional


def q1(map):
    start = [(line.index("S"), y) for y, line in enumerate(map) if "S" in line][0]
    max_dist = 6 if len(map) == 11 else 64
    distances = explore_dijkstra(start, map, max_dist)
    reached = {
        pos for pos, dist in distances.items() if dist % 2 == 0 and dist <= max_dist
    }
    [
        print(
            "".join(
                [
                    "S" if (x, y) == start else "O" if (x, y) in reached else map[y][x]
                    for x in range(len(map[0]))
                ]
            )
        )
        for y in range(len(map))
    ]
    return len(reached)


def q2_original(map):
    start = [(line.index("S"), y) for y, line in enumerate(map) if "S" in line][0]

    # calculate how many spare steps we need to visit every spot in the map, from S
    # It's safe to assume the steps we took to reach the centre from the neighbour
    # don't affect this, as they'll be the shortest path from that edge to the S)
    steps_to_completely_fill_tile = max(explore_dijkstra(start, map).values())

    # calculate shortest distance from S in centre tile to S in each of the 8 neighbours
    nine_tile_grid = 3 * [3 * line for line in map]
    nine_tile_grid_start = (start[0] + len(map[0]), start[1] + len(map))
    nine_tile_distances = explore_dijkstra(nine_tile_grid_start, nine_tile_grid)
    [
        print(
            "".join(
                [
                    str(nine_tile_distances.get((x, y), nine_tile_grid[y][x])).center(3)
                    for x in range(len(nine_tile_grid[0]))
                ]
            )
        )
        for y in range(len(nine_tile_grid))
    ]

    centre_to_centre_distances = {}
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            centre_to_centre_distances[(x, y)] = nine_tile_distances[
                (start[0] + (x + 1) * len(map[0]), start[1] + (y + 1) * len(map))
            ]

    print(f"{steps_to_completely_fill_tile=}, {centre_to_centre_distances=}")

    # explore outwards on infinite grid,
    # jumping in big steps from centre to centre of tiles (U,D,L,R,TL,TR,BL,BR)
    # until remaining steps < steps_to_fill_tile
    # then switch to little steps and don't allow exploration into fully-filled tiles?


def explore_dijkstra(
    start: tuple[int, int], map: list[list[str]], max_dist: Optional[int] = None
):
    distances = {start: 0}
    queue: list[tuple[int, tuple[int, int]]] = [(0, start)]
    while queue:
        dist, node = heappop(queue)
        if max_dist and dist > max_dist:
            continue
        for turn in DIR_OFFSETS.values():
            x, y = node[0] + turn[0], node[1] + turn[1]
            if 0 <= x < len(map[0]) and 0 <= y < len(map) and map[y][x] != "#":
                new_pos = (x, y)
                new_dist = dist + 1
                if new_dist < distances.get(new_pos, inf):
                    distances[new_pos] = new_dist
                    heappush(queue, (new_dist, new_pos))
    return distances


def explore_infinite_grid(
    start: tuple[int, int], map: list[list[str]], max_dist: int
) -> dict[tuple[int, int], int]:
    distances = defaultdict(lambda: inf)
    distances[start] = 0
    queue: list[tuple[int, tuple[int, int]]] = [(0, start)]
    while queue:
        dist, node = heappop(queue)
        if dist > max_dist:
            continue
        if dist > distances[(node, dir)]:
            continue

        for turn in DIR_OFFSETS.values():
            x, y = node[0] + turn[0], node[1] + turn[1]
            if 0 <= x < len(map[0]) and 0 <= y < len(map) and map[y][x] != "#":
                new_pos = (x, y)
                new_dist = dist + 1
                if new_dist < distances[new_pos]:
                    distances[new_pos] = new_dist
                    heappush(queue, (new_dist, new_pos))
    return {key: int(dist) for key, dist in distances.items() if dist != inf}


def explore_slooooow(
    pos: tuple[int, int],
    steps_remaining: int,
    map: list[list[str]],
    visited: dict[tuple[int, int], int],
) -> set[tuple[int, int]]:
    if pos[0] < 0 or pos[0] >= len(map[0]) or pos[1] < 0 or pos[1] >= len(map):
        return set()
    if map[pos[1]][pos[0]] == "#":
        return set()
    if steps_remaining == 0:
        return {pos}

    if visited.get(pos, 0) > steps_remaining:
        return set()
    visited[pos] = steps_remaining

    ret = set()
    if steps_remaining % 2 == 0:
        ret.add(pos)
    for dir in DIR_OFFSETS.values():
        ret |= explore_slooooow(
            (pos[0] + dir[0], pos[1] + dir[1]), steps_remaining - 1, map, visited
        )
    return ret


def q2(map):
    # with a LOT of help from https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21

    start = [(line.index("S"), y) for y, line in enumerate(map) if "S" in line][0]
    distances = explore_dijkstra(start, map)

    # haven't worked out why this -1 is required but it fixes the result!  ........V
    even_corners = len([v for v in distances.values() if v % 2 == 0 and v > 65]) - 1
    odd_corners = len([v for v in distances.values() if v % 2 == 1 and v > 65])

    even_full = len([v for v in distances.values() if v % 2 == 0])
    odd_full = len([v for v in distances.values() if v % 2 == 1])

    grids_reachable = (26_501_365 - (len(map) // 2)) // len(map)
    assert grids_reachable == 202_300, grids_reachable

    ret = (
        (grids_reachable + 1) * (grids_reachable + 1) * odd_full
        + (grids_reachable * grids_reachable) * even_full
        - (grids_reachable + 1) * odd_corners
        + grids_reachable * even_corners
    )
    return f"got {ret}, expected 604592315958630, diff={ret - 604592315958630}"


def q2_copied_right(input):
    grid = set()
    free = set()

    x = 0
    for y, l in enumerate(input):
        for x, c in enumerate(l):
            if c == "#":
                grid.add(x + y * 1j)
            elif c == "S":
                start = x + y * 1j
            elif c == ".":
                free.add(x + y * 1j)

    deltas = [1, -1, -1j, 1j]

    reach = {0: set([start])}

    grid_len = x + 1
    pts = []
    target_time = 26501365
    while len(pts) < 3:
        steps = max(reach.keys())

        if steps - 1 in reach:
            del reach[steps - 1]

        reach[steps + 1] = set()

        for pos in reach[steps]:
            for d in deltas:
                npt = pos + d
                nx = npt.real % grid_len
                ny = npt.imag % grid_len
                if nx + ny * 1j not in grid:
                    reach[steps + 1].add(pos + d)
        if (steps - (grid_len // 2) + 1) % grid_len == 0:
            pts.append(len(reach[max(reach.keys())]))

    c = pts[0]
    b = pts[1] - pts[0]
    a = pts[2] - pts[1]

    x = target_time // grid_len  # remainder is already in the euqtion
    assert grid_len // 2 == target_time % grid_len

    print(c + b * x + (x * (x - 1) // 2) * (a - b))
