from enum import Enum
import re


class Direction(Enum):
    Right = (0, 1)
    Down = (1, 0)
    Left = (0, -1)
    Up = (-1, 0)


def get_dir_from_char(char: str) -> Direction:
    match char:
        case "R":
            return Direction.Right
        case "D":
            return Direction.Down
        case "L":
            return Direction.Left
        case "U":
            return Direction.Up
        case _:
            raise RuntimeError


def parse(input: str) -> list[tuple[Direction, int]]:
    result = []

    for m in re.finditer(
        r"^(?P<dir>R|D|L|U) (?P<count>\d+) \(#[0-9a-f]{6}\)$", input, re.MULTILINE
    ):
        dir = get_dir_from_char(m["dir"])
        count = int(m["count"])

        result.append((dir, count))

    return result


def get_positions(
    instructions: list[tuple[Direction, int]]
) -> tuple[list[tuple[int, int]], int]:
    positions: list[tuple[int, int]] = [(0, 0)]
    perimeter = 0

    i, j = 0, 0
    for dir, count in instructions:
        di, dj = dir.value

        i += count * di
        j += count * dj

        positions.append((i, j))
        perimeter += count

    return positions, perimeter


def shoelace(positions: list[tuple[int, int]]) -> float:
    a = 0

    for (x_a, y_a), (x_b, y_b) in zip(positions, positions[1:]):
        a += (y_a + y_b) * (x_a - x_b) / 2

    (x_a, y_a), (x_b, y_b) = positions[-1], positions[0]
    a += (y_a + y_b) * (x_a - x_b) / 2

    return a


def solve(input: str) -> int:
    instructions = parse(input)
    positions, perimeter = get_positions(instructions)

    a = abs(shoelace(positions)) + perimeter / 2 + 1

    return int(a)


if __name__ == "__main__":
    with open("./inputs/day18.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
