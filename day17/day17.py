# https://adventofcode.com/2023/day/17


from heapq import heappop, heappush
import math
from collections import defaultdict


def q1(input):
    return dijkstra_crucible(input, 1, 3)


def q2(input):
    return dijkstra_crucible(input, 4, 10)


def dijkstra_crucible(input, min_straight, max_straight):
    source = (0, 0)
    dest = (len(input[0]) - 1, len(input) - 1)

    heatloss = defaultdict(lambda: math.inf)
    queue = [(0, (source, (0, 1))), (0, (source, (1, 0)))]
    while queue:
        so_far, (node, dir) = heappop(queue)
        if node == dest:
            return so_far
        if so_far > heatloss[(node, dir)]:
            continue
        for turn in ((-dir[1], dir[0]), (dir[1], -dir[0])):
            new_cost = so_far
            for distance in range(1, max_straight + 1):
                x, y = node[0] + turn[0] * distance, node[1] + turn[1] * distance
                if 0 <= x < len(input[0]) and 0 <= y < len(input):
                    new_cost += int(input[y][x])
                    if distance < min_straight:
                        continue
                    key = ((x, y), turn)
                    if new_cost < heatloss[key]:
                        heatloss[key] = new_cost
                        heappush(queue, (new_cost, key))
