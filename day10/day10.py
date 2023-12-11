# https://adventofcode.com/2023/day/10


from enum import Enum


# Coordinate scheme
#   0 1 . . X
# 0   a(1,0)
# 1   b(1,1)
# .
# .
# Y


# {current<char>: {neighbour1<x-offset, y-offset>, neighbour2<x-offset, y-offset>}}


CONNECTIONS = {
    "|": {(0, -1), (0, 1)},
    "-": {(-1, 0), (1, 0)},
    "L": {(0, -1), (1, 0)},
    "J": {(-1, 0), (0, -1)},
    "7": {(-1, 0), (0, 1)},
    "F": {(1, 0), (0, 1)},
}
SEARCH_SPACE = frozenset({(-1, 0), (1, 0), (0, -1), (0, 1)})


def symbol(pos, input):
    return input[pos[1]][pos[0]]


def valid_move(orig, dest, input):
    if orig == dest:
        return False
    if len(input[0]) < dest[0] < 0:
        return False
    if len(input) < dest[1] < 0:
        return False

    orig_symbol = symbol(orig, input)
    if orig_symbol != "S":
        # can we move FROM ORIG to dest?
        if (dest[0] - orig[0], dest[1] - orig[1]) not in CONNECTIONS[orig_symbol]:
            return False

    dest_symbol = symbol(dest, input)
    if dest_symbol != "S":
        # can we move TO DEST from orig?
        if dest_symbol not in CONNECTIONS:
            return False
        if (orig[0] - dest[0], orig[1] - dest[1]) not in CONNECTIONS[dest_symbol]:
            return False

    return True


def longest_route(input):
    start = [(input[y].find("S"), y) for y in range(len(input)) if "S" in input[y]][0]
    longest = []
    for root in [(s[0] + start[0], s[1] + start[1]) for s in SEARCH_SPACE]:
        if not valid_move(start, root, input):
            continue
        path = [root]
        prev = start
        current = root
        while True:
            next = [
                (n[0] + current[0], n[1] + current[1])
                for n in CONNECTIONS[symbol(current, input)]
                if (n[0] + current[0], n[1] + current[1]) != prev
            ][0]
            if not valid_move(current, next, input):
                break
            path.append(next)
            if symbol(next, input) == "S":
                if len(path) > len(longest):
                    longest = path
                break
            prev = current
            current = next
    return longest


def q1(input):
    return len(longest_route(input)) // 2


class Direction(Enum):
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"


OFFSET_TO_DIRECTION_MAP = {
    (-1, 0): Direction.LEFT,
    (1, 0): Direction.RIGHT,
    (0, -1): Direction.UP,
    (0, 1): Direction.DOWN,
}
DIRECTION_TO_OFFSET_MAP = {v: k for k, v in OFFSET_TO_DIRECTION_MAP.items()}


def travel_dir(i, pipeline):
    fr = pipeline[(i - 1) % len(pipeline)]
    to = pipeline[i % len(pipeline)]
    return OFFSET_TO_DIRECTION_MAP[(to[0] - fr[0], to[1] - fr[1])]


INSIDES_MAP = {
    ("-", Direction.RIGHT): {Direction.DOWN},
    ("-", Direction.LEFT): {Direction.UP},
    ("|", Direction.UP): {Direction.RIGHT},
    ("|", Direction.DOWN): {Direction.LEFT},
    ("F", Direction.LEFT): {Direction.UP, Direction.LEFT},
    ("7", Direction.UP): {Direction.UP, Direction.RIGHT},
    ("L", Direction.DOWN): {Direction.DOWN, Direction.LEFT},
    ("J", Direction.RIGHT): {Direction.DOWN, Direction.RIGHT},
}


def greedy_fill(symbol, candidate, state, pipeline):
    if (
        candidate[0] >= len(state[0])
        or candidate[0] < 0
        or candidate[1] >= len(state)
        or candidate[1] < 0
    ):
        return
    if candidate in pipeline:
        return
    if state[candidate[1]][candidate[0]] == symbol:
        return

    state[candidate[1]][candidate[0]] = symbol
    for offset in SEARCH_SPACE:
        greedy_fill(
            symbol,
            (candidate[0] + offset[0], candidate[1] + offset[1]),
            state,
            pipeline,
        )


def entrypoint_clockwise(pipeline, state):
    topleft_index = pipeline.index(min(pipeline))
    topleft = pipeline[topleft_index]
    symbol = state[topleft[1]][topleft[0]]
    assert symbol == "F", f"expected F, got {symbol}, at {topleft}"

    next = pipeline[topleft_index + 1]
    if next[0] == topleft[0] + 1 and next[1] == topleft[1]:
        return topleft_index, pipeline
    return entrypoint_clockwise(list(reversed(pipeline)), state)


def q2(input):
    pipeline = longest_route(input)
    state = [[c for c in line] for line in input]

    # Traverse the path clockwise,
    # from any point nearest an edge (to avoid starting on an inner loop)
    # Everything on our left is outside, everything on our right is inside
    topleft, pipeline = entrypoint_clockwise(pipeline, state)

    for i in range(topleft, topleft + len(pipeline)):
        step = pipeline[i % len(pipeline)]
        dir = travel_dir(i, pipeline)
        symbol = state[step[1]][step[0]]

        if symbol == "S":
            # maybe we can get away without handling this!
            continue

        for inside_dir in INSIDES_MAP.get((symbol, dir), set()):
            offset = DIRECTION_TO_OFFSET_MAP[inside_dir]
            candidate = (step[0] + offset[0], step[1] + offset[1])
            # print(
            #     f"  {i}: {step}({symbol}) heading {dir}: filling IN from {candidate}..."
            # )
            greedy_fill("I", candidate, state, pipeline)
            # state[step[1]][step[0]] = "@"
            # [print("".join(row)) for row in state]
            # state[step[1]][step[0]] = symbol

    [print("".join(row)) for row in state]
    return sum(
        [
            1
            for x in range(len(state[0]))
            for y in range(len(state))
            if (x, y) not in pipeline and state[y][x] == "I"
        ]
    )


####################################################################################
####################################################################################
####################################################################################


def q2_attempt_one_doesnt_work(input):
    pipeline = longest_route(input)
    state = [[c for c in line] for line in input]

    for x in range(len(state[0])):
        for y in range(len(state)):
            if (x, y) in pipeline or state[y][x] in {"O", "I"}:
                continue
            print(f"Starting trace from root node {(x, y)} ({state[y][x]})...")
            path_to_edge(
                state,
                pipeline,
                (x, y),
                (0, 0),
                {(x, y)},
            )
            [print("".join(row)) for row in state]
    return sum(
        [
            1
            for x in range(len(state[0]))
            for y in range(len(state))
            if (x, y) not in pipeline and state[y][x] != "O"
        ]
    )


# which side of the pipe are we?
# {direction : {to_symbol: result_side}}
#   X
#   012
# Y0F-7
#  1|.|
#  2L-J
SYMBOLS_TO_SIDES = {
    "-": {(0, -1), (0, 1)},
    "|": {(-1, 0), (1, 0)},
    "F": {(-1, -1), (1, 1)},
    "J": {(-1, -1), (1, 1)},
    "7": {(1, -1), (-1, 1)},
    "L": {(1, -1), (-1, 1)},
}


def path_to_edge(state, pipeline, pos, side, visited):
    if pos not in pipeline and (
        pos[0] == 0
        or pos[0] == len(state[0]) - 1
        or pos[1] == 0
        or pos[1] == len(state) - 1
    ):
        state[pos[1]][pos[0]] = "O"
        visited.resve(pos)
        return True
    # current_symbol = state[pos[1]][pos[0]]

    for neighbour_x, neighbour_y in SEARCH_SPACE:
        candidate = (pos[0] + neighbour_x, pos[1] + neighbour_y)

        if (
            candidate[0] >= len(state[0])
            or candidate[0] < 0
            or candidate[1] >= len(state)
            or candidate[1] < 0
        ):
            continue

        next_symbol = state[candidate[1]][candidate[0]]
        if next_symbol == "S":
            #  don't know how to handle these!
            continue

        moving_along_pipeline = False
        if pos in pipeline:
            # can always go to the next link in the pipeline, BUT
            # can only go to neighbours that don't involve crossing the 'side'
            ind = pipeline.index(pos)
            if candidate in {
                pipeline[ind + 1 % len(pipeline)],
                pipeline[ind - 1 % len(pipeline)],
            }:
                moving_along_pipeline = True
            elif (neighbour_x != 0 and neighbour_x != side[0]) or (
                neighbour_y != 0 and neighbour_y != side[1]
            ):
                continue

        if next_symbol in {"O", "I"}:
            if pos not in pipeline:
                state[pos[1]][pos[0]] = next_symbol
            return next_symbol == "O"

        if candidate in visited:
            continue

        # neighbour is reachable, not visited, not wrong side of pipe, but unknown state: recurse

        if candidate in pipeline:
            temp_side = (-neighbour_x, -neighbour_y)
            if moving_along_pipeline:
                temp_side = (
                    side[0] if neighbour_x == 0 else 0,
                    side[1] if neighbour_y == 0 else 0,
                )
            poss_side_1, poss_side_2 = SYMBOLS_TO_SIDES[next_symbol]
            if (poss_side_1[0] != 0 and poss_side_1[0] == temp_side[0]) or (
                poss_side_1[1] != 0 and poss_side_1[1] == temp_side[1]
            ):
                next_side = poss_side_1
            else:
                next_side = poss_side_2
        else:
            next_side = (0, 0)

        # print(
        #     f"  recursing from {pos}({current_symbol}) ({side=}) "
        #     + f"to {candidate}({next_symbol}) ({next_side=})"
        # )
        if path_to_edge(state, pipeline, candidate, next_side, visited | {candidate}):
            # print(
            #     f"  found recursive path to outside from {pos} ({current_symbol}) "
            #     + f"through {candidate}, marking O"
            # )
            if pos not in pipeline:
                state[pos[1]][pos[0]] = "O"
            visited.remove(pos)
            return True

    # didn't find any path to outside, not on pipeline, must be inside
    if pos not in pipeline:
        # print(
        #     f" found a node with no path to outside at {pos}, marking {state[pos[1]][pos[0]]} to I"
        # )
        state[pos[1]][pos[0]] = "I"
    visited.remove(pos)
    return False
