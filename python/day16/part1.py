from enum import Enum
from collections.abc import Callable
from typing import Literal


class Directions(Enum):
    Right = (0, 1)
    Down = (1, 0)
    Left = (0, -1)
    Up = (-1, 0)


Mirror = Literal[".", "|", "-", "/", "\\"]
Position = tuple[int, int]
State = tuple[Position, Directions]
NeighborsGetter = Callable[[State], list[State]]


def propagate(position: Position, direction: Directions) -> Position:
    i, j = position
    di, dj = direction.value
    return i + di, j + dj


def get_reflections(ray_direction: Directions, mirror: Mirror) -> list[Directions]:
    match mirror:
        case ".":
            return [ray_direction]
        case "|":
            match ray_direction:
                case Directions.Left | Directions.Right:
                    return [Directions.Down, Directions.Up]
                case Directions.Down | Directions.Up:
                    return [ray_direction]
        case "-":
            match ray_direction:
                case Directions.Down | Directions.Up:
                    return [Directions.Right, Directions.Left]
                case Directions.Right | Directions.Left:
                    return [ray_direction]
        case "/":
            # (di, dj) -> (-dj, -di)
            match ray_direction:
                case Directions.Right:
                    return [Directions.Up]
                case Directions.Down:
                    return [Directions.Left]
                case Directions.Left:
                    return [Directions.Down]
                case Directions.Up:
                    return [Directions.Right]
        case "\\":
            # (di, dj) -> (dj, di)
            match ray_direction:
                case Directions.Right:
                    return [Directions.Down]
                case Directions.Down:
                    return [Directions.Right]
                case Directions.Left:
                    return [Directions.Up]
                case Directions.Up:
                    return [Directions.Left]


def parse(input: str) -> NeighborsGetter:
    grid: list[list[Mirror]] = []
    for line in input.splitlines():
        grid.append([])
        for mirror in line:
            grid[-1].append(mirror)  # type: ignore

    lines_count, cols_count = len(grid), len(grid[0])

    def get_neighbors(state: State) -> list[State]:
        def is_within_boundaries(position: Position) -> bool:
            i, j = position
            return 0 <= i < lines_count and 0 <= j < cols_count

        pos, dir = state
        i, j = pos
        mirror = grid[i][j]
        new_directions = get_reflections(dir, mirror)

        neighbors = []
        for new_dir in new_directions:
            new_pos = propagate(pos, new_dir)
            if is_within_boundaries(new_pos):
                neighbors.append((new_pos, new_dir))

        return neighbors

    return get_neighbors


def dfs(start: State, get_neighbors: NeighborsGetter) -> set[State]:
    visited = set()

    def _dfs(node):
        if node in visited:
            return
        visited.add(node)
        for neighbor in get_neighbors(node):
            _dfs(neighbor)

    _dfs(start)

    return visited


def solve(input: str) -> int:
    get_neighbors = parse(input)

    start = ((0, 0), Directions.Right)
    states = dfs(start, get_neighbors)
    energized_positions = set((i, j) for (i, j), dir in states)

    return len(energized_positions)


if __name__ == "__main__":
    import sys

    sys.setrecursionlimit(10000)

    with open("./inputs/day16.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
