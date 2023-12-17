from copy import deepcopy
from itertools import count

Platform = list[list[str]]
PlatformAsTuples = tuple[tuple[str, ...], ...]


def parse(input: str) -> Platform:
    platform = []

    for line in input.splitlines():
        platform.append([c for c in line])

    return platform


def to_tuples(platform: Platform) -> PlatformAsTuples:
    return tuple(tuple(line) for line in platform)


def rotate(platform: Platform) -> Platform:
    lines_count = len(platform)
    cols_count = len(platform[0])

    return [
        [platform[i][j] for i in reversed(range(lines_count))]
        for j in range(cols_count)
    ]


def tilt_north(platform: Platform) -> Platform:
    platform = deepcopy(platform)

    lines_count = len(platform)
    cols_count = len(platform[0])

    for j in range(cols_count):
        last_static = -1
        for i in range(lines_count):
            match platform[i][j]:
                case "#":
                    last_static = i
                case ".":
                    continue
                case "O":
                    platform[i][j] = "."
                    platform[last_static + 1][j] = "O"
                    last_static = last_static + 1

    return platform


def cycle(platform: Platform) -> Platform:
    for _ in range(4):
        platform = tilt_north(platform)
        platform = rotate(platform)

    return platform


def compute_load(platform: Platform | PlatformAsTuples) -> int:
    load = 0

    n = len(platform)
    for i, line in enumerate(platform):
        load += sum(1 for c in line if c == "O") * (n - i)

    return load


def get_first_platform_transforms(
    platform: Platform,
) -> tuple[list[PlatformAsTuples], int, int]:
    platforms: list[PlatformAsTuples] = []
    cycle_start, cycle_length = -1, -1

    indices: dict[PlatformAsTuples, int] = {}
    for i in count():
        t = to_tuples(platform)
        if t in indices:
            cycle_start, cycle_length = indices[t], i - indices[t]
            break

        indices[t] = i
        platforms.append(t)

        platform = cycle(platform)

    return platforms, cycle_start, cycle_length


def solve(input: str) -> int:
    platform = parse(input)

    platforms, cycle_start, cycle_length = get_first_platform_transforms(platform)

    target = 1000000000
    cycles_to_perform = min(target, cycle_start + (target - cycle_start) % cycle_length)

    return compute_load(platforms[cycles_to_perform])


if __name__ == "__main__":
    with open("./inputs/day14.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
