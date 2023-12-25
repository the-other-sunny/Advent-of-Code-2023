from enum import Enum


class Direction(Enum):
    LEFT = (0, 1)
    DOWN = (1, 0)
    RIGHT = (0, -1)
    UP = (-1, 0)


Tile = str
Grid = list[list[Tile]]
Node = tuple[int, int]
Path = list[Node]


def is_in_grid(i: int, j: int, grid: Grid) -> bool:
    lines_count, cols_count = len(grid), len(grid[0])

    return 0 <= i < lines_count and 0 <= j < cols_count


def tile_possible_directions(tile: Tile) -> list[Direction]:
    if tile in "^>v<":
        match tile:
            case ">":
                return [Direction.LEFT]
            case "v":
                return [Direction.DOWN]
            case "<":
                return [Direction.RIGHT]
            case "^":
                return [Direction.UP]

    return list(Direction)


def get_neighbors(u: Node, grid: Grid) -> list[Node]:
    result = []
    i, j = u

    for dir in tile_possible_directions(grid[i][j]):
        di, dj = dir.value

        next_i = i + di
        next_j = j + dj

        if is_in_grid(next_i, next_j, grid) and grid[next_i][next_j] != "#":
            result.append((next_i, next_j))

    return result


def parse(input: str) -> tuple[Grid, Node, Node]:
    grid = [list(line) for line in input.splitlines()]

    lines_count = len(grid)
    start = (0, grid[0].index("."))
    end = (lines_count - 1, grid[-1].index("."))

    return grid, start, end


def get_all_simple_paths(start: Node, end: Node, grid: Grid) -> list[Path]:
    paths = []

    path = [start]
    visited = {start}

    def explore(u: tuple[int, int]):
        if u == end:
            paths.append(path.copy())
            return

        for v in get_neighbors(u, grid):
            if v in visited:
                continue

            visited.add(v)
            path.append(v)

            explore(v)

            path.pop()
            visited.remove(v)

    explore(start)

    return paths


def solve(input: str) -> int:
    grid, start, end = parse(input)

    simple_paths = get_all_simple_paths(start, end, grid)

    return max(len(path) - 1 for path in simple_paths)


if __name__ == "__main__":
    import sys

    sys.setrecursionlimit(5000)

    with open("./inputs/day23.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
