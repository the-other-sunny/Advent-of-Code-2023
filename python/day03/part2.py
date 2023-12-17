import re
from collections import defaultdict
from math import prod

NumberLocation = tuple[int, int, int]
Position = tuple[int, int]


def is_gear(c: str) -> bool:
    return c == "*"


def is_gear_at(line_index: int, col_index: int, lines: list[str]) -> bool:
    lines_count, cols_count = len(lines), len(lines[0])

    return (
        0 <= line_index < lines_count
        and 0 <= col_index < cols_count
        and is_gear(lines[line_index][col_index])
    )


def get_neighboring_positions(number_location: NumberLocation) -> list[Position]:
    line_index, start, end = number_location
    neighbors = [(line_index, start - 1), (line_index, end)]

    for col_index in range(start - 1, end + 1):
        neighbors.append((line_index - 1, col_index))
        neighbors.append((line_index + 1, col_index))

    return neighbors


def get_numbers_locations(lines: list[str]) -> list[tuple[int, NumberLocation]]:
    locations = []

    for line_index, line in enumerate(lines):
        for regex_match in re.finditer("\d+", line):
            number = int(regex_match[0])
            start, end = regex_match.span()
            locations.append((number, (line_index, start, end)))

    return locations


def get_gears_neighboring_numbers(lines: list[str]) -> defaultdict[Position, list[int]]:
    gears_neighboring_numbers = defaultdict(list)

    for number, location in get_numbers_locations(lines):
        for i, j in get_neighboring_positions(location):
            if is_gear_at(i, j, lines):
                gear_position = (i, j)
                gears_neighboring_numbers[gear_position].append(number)

    return gears_neighboring_numbers


def solve(input: str) -> int:
    lines = input.splitlines()

    return sum(
        prod(neighboring_numbers)
        for _, neighboring_numbers in get_gears_neighboring_numbers(lines).items()
        if len(neighboring_numbers) == 2
    )


if __name__ == "__main__":
    with open("./inputs/day03.txt", mode="r", encoding="utf-8") as file:
        input = file.read()

    answer = solve(input)
    print(f"{answer = }")
