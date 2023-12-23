from __future__ import annotations
from collections import defaultdict
from typing import NamedTuple, override
from itertools import product
from functools import total_ordering
from queue import Queue


class Vec2(NamedTuple):
    x: int = 0
    y: int = 0


@total_ordering
class Vec3(NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0

    @override
    def __add__(self, other: tuple) -> Vec3:
        if not isinstance(other, Vec3):
            raise TypeError

        x_a, y_a, z_a = self
        x_b, y_b, z_b = other

        return Vec3(x_a + x_b, y_a + y_b, z_a + z_b)

    def __le__(self, other: tuple) -> bool:
        if not isinstance(other, Vec3):
            raise TypeError

        x_a, y_a, z_a = self
        x_b, y_b, z_b = other

        return (z_a, x_a, y_a) <= (z_b, x_b, y_b)


class Brick(NamedTuple):
    start: Vec3
    end: Vec3

    @property
    def base(self) -> set[Vec2]:
        x_a, y_a, z_a = self.start
        x_b, y_b, z_b = self.end

        return set(
            Vec2(x, y)
            for x, y, _ in product(
                range(x_a, x_b + 1), range(y_a, y_b + 1), range(z_a, z_b + 1)
            )
        )

    def with_height(self, new_z: int) -> Brick:
        dz = new_z - self.start.z

        return Brick(self.start + Vec3(0, 0, dz), self.end + Vec3(0, 0, dz))


FLOOR = Brick(Vec3(), Vec3())


def parse(input: str) -> list[Brick]:
    bricks = []

    for line in input.splitlines():
        s, _, e = line.partition("~")
        start = Vec3(*(int(v) for v in s.split(",")))
        end = Vec3(*(int(v) for v in e.split(",")))

        if end < start:
            start, end = end, start

        bricks.append(Brick(start, end))

    return bricks


def get_max_with_args(table: dict[Brick, int]) -> tuple[int | None, list[Brick]]:
    max = None
    args = []
    for arg in table:
        value = table[arg]

        if max is None or value > max:
            max = value
            args = [arg]
        elif value == max:
            args.append(arg)

    return max, args


AfterFallData = tuple[list[Brick], dict[Brick, list[Brick]]]


def get_support_data_after_fall(bricks: list[Brick]) -> AfterFallData:
    bricks = sorted(bricks, key=lambda b: b.start.z)
    max_heights: dict[Vec2, tuple[int, Brick]] = defaultdict(lambda: (0, FLOOR))

    bricks_supported_by = defaultdict(list)

    for i, brick in enumerate(bricks):
        heights_table = {
            brick: height for height, brick in (max_heights[pos] for pos in brick.base)
        }

        available_height, supporting_bricks = get_max_with_args(heights_table)

        assert available_height is not None

        brick = bricks[i] = brick.with_height(available_height + 1)

        for pos in brick.base:
            max_heights[pos] = (brick.end.z, brick)

        for supporting_brick in supporting_bricks:
            bricks_supported_by[supporting_brick].append(brick)

    return bricks, bricks_supported_by


def count_unsupported_bricks(removed_brick, bricks_supported_by):
    supports_count = defaultdict(int)
    for u, neighbors in bricks_supported_by.items():
        for v in neighbors:
            supports_count[v] += 1

    q = Queue()
    for u in bricks_supported_by[removed_brick]:
        q.put_nowait(u)

    while not q.empty():
        u = q.get_nowait()

        supports_count[u] -= 1
        if supports_count[u] != 0:
            continue

        for v in bricks_supported_by[u]:
            q.put_nowait(v)

    return sum(1 for count in supports_count.values() if count == 0)


def solve(input: str) -> int:
    bricks = parse(input)
    bricks, bricks_supported_by = get_support_data_after_fall(bricks)

    return sum(
        count_unsupported_bricks(removed_brick, bricks_supported_by)
        for removed_brick in bricks
    )


if __name__ == "__main__":
    with open("./inputs/day22.txt", encoding="utf-8") as file:
        input = file.read()

    answer = solve(input)
    print(f"{answer = }")
