# https://adventofcode.com/2023/day/22

from dataclasses import dataclass
from itertools import combinations_with_replacement
from collections import defaultdict


@dataclass
class Cube:
    x: int
    y: int
    z: int


@dataclass
class Brick:
    name: str
    start: Cube
    end: Cube

    def xy_plane(self):
        x_incr = 1 if self.start.x <= self.end.x else -1
        y_incr = 1 if self.start.y <= self.end.y else -1
        return {
            (x, y)
            for x in range(self.start.x, self.end.x + x_incr, x_incr)
            for y in range(self.start.y, self.end.y + y_incr, y_incr)
        }


def q1(input):
    settled_bricks = settle_bricks(input)

    disintegratable_bricks = []
    for brick in settled_bricks:
        # look at all the cells above this brick's top layer, see if any bricks are resting on it
        # for each of those bricks, see if they're resting on anything else
        # if not, this brick is not disintegratable
        disintegratable = True
        top = max(brick.start.z, brick.end.z)
        for brick_above in filter(
            lambda b: b.start.z == top + 1
            and not b.xy_plane().isdisjoint(brick.xy_plane()),
            settled_bricks,
        ):
            unsupported_cubes = brick_above.xy_plane() - brick.xy_plane()
            if not any(
                filter(
                    lambda b: b.end.z == top  # type: ignore
                    and not b.xy_plane().isdisjoint(unsupported_cubes),  # type: ignore
                    settled_bricks,
                )
            ):
                disintegratable = False
                break

        if disintegratable:
            disintegratable_bricks.append(brick)

    return len(disintegratable_bricks)


def q2(input):
    settled_bricks = settle_bricks(input)

    supporting = {
        brick.name: {
            brick_above.name
            for brick_above in filter(
                lambda b: b.start.z == brick.end.z + 1
                and not b.xy_plane().isdisjoint(brick.xy_plane()),
                settled_bricks,
            )
        }
        for brick in settled_bricks
    }

    supported_by = defaultdict(set)
    for under, aboves in supporting.items():
        for above in aboves:
            supported_by[above].add(under)

    # for each brick in supporting, BFS up through what it's supporting,
    # collecting a set of everything that's been disintegrated.
    # For each brick we reach, disintegrate it if there aren't any remaining entries
    # in the dependencies set after removing the set of what's already been disintegrated
    cascades = {
        brick.name: collapses(brick.name, supporting, supported_by, set())
        - {brick.name}
        for brick in settled_bricks
    }
    # print(cascades)
    return sum([len(v) for v in cascades.values()])


def collapses(name, supporting, supported_by, disintegrated: set[str]) -> set[str]:
    disintegrated.add(name)
    will_collapse = set(
        {above for above in supporting[name] if not supported_by[above] - disintegrated}
    )

    for brick in will_collapse:
        collapses(brick, supporting, supported_by, disintegrated)

    return disintegrated


def settle_bricks(input: list[str]) -> list[Brick]:
    names = map(
        lambda t: "".join(t),
        combinations_with_replacement("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 3),
    )
    falling_bricks = [
        Brick(
            next(names),
            Cube(*[int(n) for n in start.split(",")]),
            Cube(*[int(n) for n in end.split(",")]),
        )
        for start, end in [line.split("~") for line in input]
    ]

    settled_bricks = []
    current_heights = {}
    for brick in sorted(falling_bricks, key=lambda b: min(b.start.z, b.end.z)):
        min_z = max([current_heights.get(p, 0) + 1 for p in brick.xy_plane()])

        brick_height = abs(brick.start.z - brick.end.z)
        brick.start.z = min_z
        brick.end.z = min_z + brick_height

        for p in brick.xy_plane():
            current_heights[p] = brick.end.z
        settled_bricks.append(brick)

    return settled_bricks
