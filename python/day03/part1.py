import re

NumberLocation = tuple[int, int, int]
Position = tuple[int, int]


def is_symbol(c: str) -> bool:
    return c != "."


def is_symbol_at(line_index: int, col_index: int, lines: list[str]) -> bool:
    lines_count, cols_count = len(lines), len(lines[0])

    return (
        0 <= line_index < lines_count
        and 0 <= col_index < cols_count
        and is_symbol(lines[line_index][col_index])
    )


def get_neighboring_positions(number_location: NumberLocation) -> list[Position]:
    line_index, start, end = number_location
    neighbors = [(line_index, start - 1), (line_index, end)]

    for col_index in range(start - 1, end + 1):
        neighbors.append((line_index - 1, col_index))
        neighbors.append((line_index + 1, col_index))

    return neighbors


def is_part_number_at(number_location: NumberLocation, lines: list[str]) -> bool:
    return any(
        is_symbol_at(i, j, lines) for i, j in get_neighboring_positions(number_location)
    )


def get_numbers_locations(lines: list[str]) -> list[tuple[int, NumberLocation]]:
    locations = []

    for line_index, line in enumerate(lines):
        for regex_match in re.finditer("\d+", line):
            number = int(regex_match[0])
            start, end = regex_match.span()
            locations.append((number, (line_index, start, end)))

    return locations


def solve(input: str) -> int:
    lines = input.splitlines()

    return sum(
        number
        for (number, number_location) in get_numbers_locations(lines)
        if is_part_number_at(number_location, lines)
    )


if __name__ == "__main__":
    with open("./inputs/day03.txt", mode="r", encoding="utf-8") as file:
        input = file.read()

    answer = solve(input)
    print(f"{answer = }")
