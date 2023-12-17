def parse(input: str) -> tuple[list[tuple[int, int]], set[int], set[int]]:
    coords = []

    lines = input.splitlines()

    unused_lines = set(range(len(lines)))
    unused_columns = set(range(len(lines[0])))

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                coords.append((i, j))
                if i in unused_lines:
                    unused_lines.remove(i)
                if j in unused_columns:
                    unused_columns.remove(j)

    return coords, unused_lines, unused_columns


def fix_coords(
    coords: list[tuple[int, int]], unused_lines: set[int], unused_columns: set[int]
) -> list[tuple[int, int]]:
    new_coords = []

    for i, j in coords:
        delta_i = sum(1 for line_i in unused_lines if line_i < i)
        delta_j = sum(1 for column_j in unused_columns if column_j < j)
        new_coords.append((i + delta_i, j + delta_j))

    return new_coords


def distance(point_a: tuple[int, int], point_b: tuple[int, int]) -> int:
    return abs(point_b[0] - point_a[0]) + abs(point_b[1] - point_a[1])


def solve(input: str) -> int:
    answer = 0

    coords, unsed_lines, unsed_columns = parse(input)
    coords = fix_coords(coords, unsed_lines, unsed_columns)

    for i in range(len(coords)):
        for j in range(i):
            answer += distance(coords[i], coords[j])

    return answer


if __name__ == "__main__":
    with open("./inputs/day11.txt", encoding="utf-8") as file:
        input = file.read()

    answer = solve(input)
    print(f"{answer = }")
