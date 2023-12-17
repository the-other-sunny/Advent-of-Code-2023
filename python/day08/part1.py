import re
from collections.abc import Callable
from typing import Literal

Node = str
Instruction = Literal["LR"]


def parse(input: str) -> tuple[list[Instruction], Callable[[Node, Instruction], Node]]:
    lines = input.splitlines()

    instructions: list[Instruction] = list(lines[0])  # type: ignore
    neighbors = {}

    for line in lines[2:]:
        m = re.fullmatch(
            r"(?P<Node>\w{3}) = \((?P<LeftNeighbor>\w{3}), (?P<RightNeighbor>\w{3})\)",
            line,
        )
        assert m is not None
        neighbors[m["Node"]] = (m["LeftNeighbor"], m["RightNeighbor"])

    def get_next(node: Node, instruction: Instruction) -> Node:
        return neighbors[node][0 if instruction == "L" else 1]

    return instructions, get_next


def solve(input: str) -> int:
    instructions, get_next = parse(input)

    steps = 0
    current_node = "AAA"

    while current_node != "ZZZ":
        for instruction in instructions:
            current_node = get_next(current_node, instruction)
            steps += 1

            if current_node == "ZZZ":
                break

    return steps


if __name__ == "__main__":
    with open("./inputs/day08.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
