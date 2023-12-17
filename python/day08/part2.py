import re
from math import lcm
from collections.abc import Callable
from typing import Literal

Node = str
Instruction = Literal["LR"]


def parse(
    input: str,
) -> tuple[list[Instruction], set[Node], Callable[[Node, Instruction], Node]]:
    lines = input.splitlines()

    instructions: list[Instruction] = list(lines[0])  # type: ignore

    starting_nodes = set()
    neighbors = {}

    for line in lines[2:]:
        m = re.fullmatch(
            r"(?P<Node>\w{3}) = \((?P<LeftNeighbor>\w{3}), (?P<RightNeighbor>\w{3})\)",
            line,
        )

        assert m is not None, line

        node, left_neighbor, right_neighbor = (
            m["Node"],
            m["LeftNeighbor"],
            m["RightNeighbor"],
        )

        if node.endswith("A"):
            starting_nodes.add(node)

        neighbors[node] = (left_neighbor, right_neighbor)

    def get_next(node: Node, instruction: Instruction) -> Node:
        return neighbors[node][0 if instruction == "L" else 1]

    return instructions, starting_nodes, get_next


def solve(input: str) -> int:
    instructions, starting_nodes, get_neighbor = parse(input)

    steps_per_starting_node = []
    for node in starting_nodes:
        steps = 0

        stop = False
        while not stop:
            for instruction in instructions:
                node = get_neighbor(node, instruction)
                steps += 1
                if node.endswith("Z"):
                    stop = True
                    break

        steps_per_starting_node.append(steps)

    return lcm(*steps_per_starting_node)


if __name__ == "__main__":
    with open("./inputs/day08.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
