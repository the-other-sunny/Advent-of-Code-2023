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


def get_tile(pos: Position, grid: Grid) -> Tile:
    i, j = pos
    lines_count, cols_count = len(grid), len(grid[0])

    return grid[i % lines_count][j % cols_count]


def get_neighbors(pos: Position, grid: Grid) -> list[Position]:
    result = []
    i, j = pos

    for dir in Direction:
        di, dj = dir.value

        new_i, new_j = i + di, j + dj
        new_pos = new_i, new_j

        if get_tile(new_pos, grid) == Tile.GARDEN_PLOT:
            result.append(new_pos)

    return result


def positions_after_steps(
    starting_positions: list[Position], steps: int, grid: Grid
) -> set[Position]:
    positions = set(starting_positions)

    for _ in range(steps):
        new_positions: set[Position] = set()

        for pos in positions:
            new_positions.update(get_neighbors(pos, grid))

        positions = new_positions

    return positions


def solve(input: str, steps=26501365) -> int:
    grid, starting_pos = parse(input)

    positions = positions_after_steps([starting_pos], 2 * 131 + 65, grid)

    def filter(I, J):
        return len(
            set(
                (i, j)
                for i, j in positions
                if (I * 131 <= i < (I + 1) * 131 and J * 131 <= j < (J + 1) * 131)
            )
        )

    assert (steps - 65) % 131 == 0

    x = (steps - 65) // 131

    corners = sum(filter(i, j) for (i, j) in [(0, 2), (0, -2), (2, 0), (-2, 0)])
    slim_diags = sum(filter(i, j) for (i, j) in [(1, 2), (-1, 2), (1, -2), (-1, -2)])
    fat_diags = sum(filter(i, j) for (i, j) in [(1, 1), (1, -1), (-1, -1), (-1, 1)])
    center = filter(0, 0)
    non_center = filter(0, 1)

    return (
        non_center * x**2
        + center * (x - 1) ** 2
        + corners
        + slim_diags * x
        + fat_diags * (x - 1)
    )


if __name__ == "__main__":
    with open("./inputs/day21.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
