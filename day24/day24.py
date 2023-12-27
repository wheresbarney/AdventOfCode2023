# https://adventofcode.com/2023/day/24

from dataclasses import dataclass
from functools import lru_cache
from typing import Optional
from z3 import RealVector, Solver


@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int
    z: int


@dataclass(unsafe_hash=True)
class Stone:
    pos: Point
    vel: Point

    @lru_cache
    def slope(self) -> tuple[int, int, int]:
        # A = y2 - y1; B = x1 - x2; C = y1 × (x2 - x1) - (y2 - y1) × x1.
        # https://www.omnicalculator.com/math/line-equation-from-two-points#:~:text=To%20compute%20the%20equation%20of,an%20b%20computed%20as%20above.
        a = self.vel.y
        b = -self.vel.x
        c = self.pos.y * self.vel.x - self.pos.x * self.vel.y
        return a, b, c


def q1(input):
    # For each pair of lines:
    # 1. Calculate each line's slope in standard form (Ax + By + C = 0), from the two points
    #     A = y2 - y1; B = x2 - x1; C = y1 × (x2 - x1) - (y2 - y1) × x1.
    #     https://www.omnicalculator.com/math/line-equation-from-two-points#:~:text=To%20compute%20the%20equation%20of,an%20b%20computed%20as%20above.
    # 2. Calculate the intercept point:
    #     (x0, y0) = ((b1c2 - b2c2)/(a1b2 - a2b1), (c1a2 - c2a1)/(a1b2, a2b1))
    #     https://www.cuemath.com/geometry/intersection-of-two-lines/
    # 3. If the intercept point is outside the sample area, continue
    # 4. [SKIP, for now!] Calculate the time the two stones reach the intercept point
    #        and test for equality

    stones = [
        Stone(
            Point(*[int(n) for n in t[0].split()]),
            Point(*[int(n) for n in t[1].split()]),
        )
        for t in [line.replace(",", "").split("@") for line in input]
    ]

    sample_range = (7, 27) if len(input) == 5 else (200000000000000, 400000000000000)

    intersections = 0
    for i, stone in enumerate(stones):
        for other in stones[i + 1 :]:  # noqa: E203
            ix, iy = intercept_xy(stone, other)
            # print(
            #     f"{(ix, iy)} for {stone=}(slope={stone.slope()}) {other=}(slope={other.slope()})"
            # )
            if (
                ix
                and iy
                and sample_range[0] <= ix <= sample_range[1]
                and sample_range[0] <= iy <= sample_range[1]
                # check the interception is in the future not the past!
                and (ix - stone.pos.x) / stone.vel.x > 0
                and (ix - other.pos.x) / other.vel.x > 0
                and (iy - stone.pos.y) / stone.vel.y > 0
                and (iy - other.pos.y) / other.vel.y > 0
            ):
                # print(
                #     f"BANG: {(ix, iy)} for {stone=}(slope={stone.slope()}) {other=}(slope={other.slope()})"
                # )
                intersections += 1

    return intersections


def intercept_xy(stone: Stone, other: Stone) -> tuple[Optional[float], Optional[float]]:
    # (x0, y0) = ((b1c2 - b2c2)/(a1b2 - a2b1), (c1a2 - c2a1)/(a1b2, a2b1))
    # https://www.cuemath.com/geometry/intersection-of-two-lines/

    a1, b1, c1 = stone.slope()
    a2, b2, c2 = other.slope()
    try:
        ix = (b1 * c2 - b2 * c1) / (a1 * b2 - a2 * b1)
        iy = (c1 * a2 - c2 * a1) / (a1 * b2 - a2 * b1)
        return ix, iy
    except ZeroDivisionError:
        return None, None


def q2(input):
    stones = [
        Stone(
            Point(*[int(n) for n in t[0].split()]),
            Point(*[int(n) for n in t[1].split()]),
        )
        for t in [line.replace(",", "").split("@") for line in input]
    ]

    throw_x, throw_y, throw_z, throw_dx, throw_dy, throw_dz = RealVector("sol", 6)
    times = RealVector("t", len(stones))
    solver = Solver()

    for time, stone in zip(times, stones):
        solver.add(throw_x + time * throw_dx == stone.pos.x + time * stone.vel.x)
        solver.add(throw_y + time * throw_dy == stone.pos.y + time * stone.vel.y)
        solver.add(throw_z + time * throw_dz == stone.pos.z + time * stone.vel.z)

    solver.check()

    print(sum(solver.model()[v].as_long() for v in (throw_x, throw_y, throw_z)))
