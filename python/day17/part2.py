from __future__ import annotations
from enum import Enum
from math import inf
from typing import NamedTuple
from collections.abc import Callable
from itertools import product
from dataclasses import dataclass, field
from heapq import heappush, heappop


@dataclass(order=True)
class Entry[T]:
    priority: float
    # `None` is used as a placeholder for a value that's not of type `T`, it's a bad design choice if `None` can be an instance of `T`
    node: T | None = field(compare=False)


class PriorityQueue[T]:
    def __init__(self) -> None:
        self._hq = []
        self._node_to_entry: dict[T, Entry[T]] = {}

    def push(self, node: T, priority: float) -> None:
        if node in self._node_to_entry:
            self.remove(node)

        entry = Entry(priority, node)
        heappush(self._hq, entry)

        self._node_to_entry[node] = entry

    def pop(self) -> tuple[T, float]:
        while self._hq:
            entry = heappop(self._hq)

            if entry.node is not None:
                del self._node_to_entry[entry.node]
                return entry.node, entry.priority

        raise KeyError

    def remove(self, node: T) -> None:
        if node not in self._node_to_entry:
            raise KeyError

        entry = self._node_to_entry.pop(node)
        entry.node = None

    def __contains__(self, node: T) -> bool:
        return node in self._node_to_entry

    def __len__(self) -> int:
        return len(self._node_to_entry)


class Direction(Enum):
    Right = (0, 1)
    Down = (1, 0)
    Left = (0, -1)
    Up = (-1, 0)

    def opposite(self) -> Direction:
        di, dj = self.value
        return Direction((-di, -dj))


class Node(NamedTuple):
    pos: tuple[int, int]
    dir: Direction | None


NeighborsGetter = Callable[[Node], list[tuple[Node, int]]]
Grid = list[list[int]]


def parse(input: str) -> tuple[list[list[int]], set[Node], NeighborsGetter]:
    grid = []
    for line in input.splitlines():
        grid.append([int(c) for c in line])

    lines_count = len(grid)
    cols_count = len(grid[0])

    nodes = set(
        Node((i, j), dir)
        for i, j, dir in product(range(lines_count), range(cols_count), Direction)
    )
    nodes.add(Node((0, 0), None))

    def is_within_boundaries(i: int, j: int) -> bool:
        return 0 <= i < lines_count and 0 <= j < cols_count

    def get_neighbors_with_costs(node: Node) -> list[tuple[Node, int]]:
        result = []

        (i, j), prev_dir = node
        for dir in Direction:
            if prev_dir is not None and (dir == prev_dir or dir == prev_dir.opposite()):
                continue

            new_i, new_j = i, j
            di, dj = dir.value
            cost = 0

            for steps in range(1, 11):
                new_i += di
                new_j += dj

                if not is_within_boundaries(new_i, new_j):
                    break

                cost += grid[new_i][new_j]

                if 4 <= steps <= 10:
                    new_node = Node((new_i, new_j), dir)

                    result.append((new_node, cost))

        return result

    return grid, nodes, get_neighbors_with_costs


def dijkstra(
    source: Node, nodes: set[Node], get_neighbors_with_costs: NeighborsGetter
) -> dict[Node, float]:
    dist = {}

    q: PriorityQueue[Node] = PriorityQueue()
    for u in nodes:
        dist[u] = inf if u != source else 0
        q.push(u, dist[u])

    while q:
        u, _ = q.pop()
        for v, cost in get_neighbors_with_costs(u):
            if v not in q:
                continue

            d = dist[u] + cost
            if d < dist[v]:
                dist[v] = d
                q.push(v, dist[v])

    return dist


def solve(input: str) -> int:
    grid, nodes, get_neighbors_with_costs = parse(input)
    dist = dijkstra(Node((0, 0), None), nodes, get_neighbors_with_costs)

    lines_count, cols_count = len(grid), len(grid[0])
    ends = [
        Node((lines_count - 1, cols_count - 1), Direction.Down),
        Node((lines_count - 1, cols_count - 1), Direction.Right),
    ]

    return int(min(dist[end] for end in ends))


if __name__ == "__main__":
    with open("./inputs/day17.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
