from __future__ import annotations
from enum import Enum
from itertools import product

Position = tuple[int, int]


class Dirs(Enum):
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)
    NORTH = (-1, 0)

    def opposite(self) -> Dirs:
        di, dj = self.value
        for dir in Dirs:
            if dir.value == (-di, -dj):
                return dir

        raise RuntimeError


def move(pos: Position, direction: Dirs) -> Position:
    i, j = pos
    di, dj = direction.value
    return (i + di, j + dj)


class Tile:
    def __init__(self, tile_str: str) -> None:
        self.type = tile_str
        match tile_str:
            case "|":
                self._directions = {Dirs.NORTH, Dirs.SOUTH}
            case "-":
                self._directions = {Dirs.EAST, Dirs.WEST}
            case "L":
                self._directions = {Dirs.NORTH, Dirs.EAST}
            case "J":
                self._directions = {Dirs.NORTH, Dirs.WEST}
            case "7":
                self._directions = {Dirs.SOUTH, Dirs.WEST}
            case "F":
                self._directions = {Dirs.SOUTH, Dirs.EAST}
            case ".":
                self._directions = set()
            case "S":
                self._directions = {dir for dir in Dirs}
            case _:
                raise RuntimeError

    def has_direction(self, direction: Dirs) -> bool:
        return direction in self._directions


class Grid:
    def __init__(self, input: str) -> None:
        self._grid = []
        for line in input.splitlines():
            self._grid.append([Tile(c) for c in line])

        self.lines_count = len(self._grid)
        self.columns_count = len(self._grid[0])

        self.starting_pos = self.find_starting_pos()

        i, j = self.starting_pos
        self._grid[i][j] = Tile("|")  # TODO: hardcoded, fix it maybe

    def has_position(self, pos: Position) -> bool:
        i, j = pos
        return 0 <= i < self.lines_count and 0 <= j < self.columns_count

    def tile_at(self, pos: Position) -> Tile:
        i, j = pos
        return self._grid[i][j]

    def find_starting_pos(self) -> Position:
        for pos in product(range(self.lines_count), range(self.columns_count)):
            if self.tile_at(pos).type == "S":
                return pos
        raise RuntimeError

    def get_neighbors(self, pos: Position) -> set[Position]:
        return set(
            move(pos, dir) for dir in Dirs if self.tile_at(pos).has_direction(dir)
        )

    def get_loop_positions(self) -> set[Position]:
        positions = {self.starting_pos}

        prev_pos = self.starting_pos
        curr_pos = self.get_neighbors(prev_pos).pop()
        while curr_pos != self.starting_pos:
            positions.add(curr_pos)

            next_pos = (self.get_neighbors(curr_pos) - {prev_pos}).pop()
            prev_pos, curr_pos = curr_pos, next_pos

        return positions


def solve(input: str) -> int:
    grid = Grid(input)
    loop_length = len(grid.get_loop_positions())
    return loop_length // 2


if __name__ == "__main__":
    with open("./inputs/day10.txt", encoding="utf-8") as file:
        input = file.read()

    answer = solve(input)
    print(f"{answer = }")
