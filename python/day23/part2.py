from enum import Enum
from itertools import product


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


def get_neighbors(u: Node, grid: Grid) -> list[Node]:
    result = []
    i, j = u

    for dir in Direction:
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


def get_simplified_graph(grid: Grid) -> dict[Node, dict[Node, int]]:
    lines_count, cols_count = len(grid), len(grid[0])

    neighbors_of: dict[Node, dict[Node, int]] = {}
    for i, j in product(range(lines_count), range(cols_count)):
        if grid[i][j] == "#":
            continue

        u = i, j

        neighbors_of[u] = {}

        for v in get_neighbors(u, grid):
            neighbors_of[u][v] = 1

    # simplification starts here
    nodes_to_remove = [u for u in neighbors_of if len(neighbors_of[u]) == 2]

    for u in nodes_to_remove:
        v1, v2 = neighbors_of[u].keys()

        neighbors_of[v1][v2] = neighbors_of[v1][u] + neighbors_of[u][v2]
        neighbors_of[v2][v1] = neighbors_of[v2][u] + neighbors_of[u][v1]

        del neighbors_of[u]
        del neighbors_of[v1][u]
        del neighbors_of[v2][u]

    return neighbors_of


def get_longuest_simple_path_length(
    start: Node, end: Node, neighbors_of: dict[Node, dict[Node, int]]
) -> int:
    max_length = -1

    length = 0
    visited = {start}

    def explore(u: tuple[int, int]):
        nonlocal length, max_length

        if u == end:
            max_length = max(max_length, length)
            return

        for v in neighbors_of[u]:
            if v in visited:
                continue

            visited.add(v)
            length += neighbors_of[u][v]

            explore(v)

            length -= neighbors_of[u][v]
            visited.remove(v)

    explore(start)

    return max_length


def solve(input: str) -> int:
    grid, start, end = parse(input)

    neighbors_of = get_simplified_graph(grid)

    return get_longuest_simple_path_length(start, end, neighbors_of)


if __name__ == "__main__":
    with open("./inputs/day23.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
