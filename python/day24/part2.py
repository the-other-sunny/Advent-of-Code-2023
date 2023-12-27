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

        positions.append(pos)
        velocities.append(v)

    return positions, velocities


def cross_product_matrix(a: NDArray) -> NDArray:
    """returns the matrix associated with the linear operation b -> a x b"""
    i, j, k = np.identity(3)

    return np.array([np.cross(a, i), np.cross(a, j), np.cross(a, k)]).T


def solve(input: str) -> int:
    # find p and v_p such that (p - a) x (v_p - v_a) = 0 for all a...
    positions, velocities = parse(input)

    a, v_a = positions[0], velocities[0]

    for (b, v_b), (c, v_c) in combinations(zip(positions[1:], velocities[1:]), 2):
        M = np.empty((6, 6))
        M[0:3, 0:3] = cross_product_matrix(v_a - v_b)
        M[0:3, 3:6] = cross_product_matrix(b - a)
        M[3:6, 0:3] = cross_product_matrix(v_a - v_c)
        M[3:6, 3:6] = cross_product_matrix(c - a)

        Y = np.concatenate(
            (np.cross(b, v_b) - np.cross(a, v_a), np.cross(c, v_c) - np.cross(a, v_a))
        )

        try:
            X = np.linalg.solve(M, Y)
        except LinAlgError:
            continue

        # p, v_p = X[:3], X[3:]
        return round(X[:3].sum())

    raise RuntimeError


if __name__ == "__main__":
    with open("./inputs/day24.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
