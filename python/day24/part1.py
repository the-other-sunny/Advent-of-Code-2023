from itertools import combinations

import numpy as np
from numpy.typing import NDArray
from numpy.linalg import LinAlgError


def parse(input: str) -> tuple[list[NDArray], list[NDArray]]:
    positions = []
    velocities = []

    for line in input.splitlines():
        left, _, right = line.partition("@")
        pos = np.array([int(x) for x in left.split(", ")])  # type: ignore
        v = np.array([int(x) for x in right.split(", ")])  # type: ignore

        positions.append(pos[:2])
        velocities.append(v[:2])

    return positions, velocities


def solve(input: str, min: int = int(2e14), max: int = int(4e14)) -> int:
    positions, velocities = parse(input)

    answer = 0

    for (a, v_a), (b, v_b) in combinations(zip(positions, velocities), 2):
        M = np.array([v_a, -v_b]).T

        try:
            t_a, t_b = np.linalg.solve(M, b - a)
        except LinAlgError:
            continue

        if t_a < 0 or t_b < 0:
            continue

        x, y = a + t_a * v_a

        if min <= x <= max and min <= y <= max:
            answer += 1

    return answer


if __name__ == "__main__":
    with open("./inputs/day24.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
