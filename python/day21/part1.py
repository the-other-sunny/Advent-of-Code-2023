from enum import Enum


class Direction(Enum):
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
    UP = (-1, 0)


class Tile(Enum):
    ROCK = "#"
    GARDEN_PLOT = "."


type Position = tuple[int, int]
type Grid = list[list[Tile]]


def parse(input: str) -> tuple[Grid, Position]:
    grid: list[list[Tile]] = []
    starting_pos = -1, -1
    for i, line in enumerate(input.splitlines()):
        grid.append([])
        for j, char in enumerate(line):
            if char == "S":
                starting_pos = i, j
                char = "."

            grid[i].append(Tile(char))

    return grid, starting_pos


def get_neighbors(pos: Position, grid: Grid) -> list[Position]:
    def is_in_grid(pos: Position, grid: Grid) -> bool:
        i, j = pos
        lines_count, cols_count = len(grid), len(grid[0])

        return 0 <= i < lines_count and 0 <= j < cols_count

    result = []
    i, j = pos

    for dir in Direction:
        di, dj = dir.value

        new_i, new_j = i + di, j + dj
        new_pos = new_i, new_j

        if is_in_grid(new_pos, grid) and grid[new_i][new_j] == Tile.GARDEN_PLOT:
            result.append(new_pos)

    return result


def solve(input: str, steps = 64) -> int:
    grid, starting_pos = parse(input)

    positions = {starting_pos}

    for _ in range(steps):
        new_positions: set[Position] = set()

        for pos in positions:
            new_positions.update(get_neighbors(pos, grid))
        positions = new_positions

    return len(positions)


if __name__ == "__main__":
    with open("./inputs/day21.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
