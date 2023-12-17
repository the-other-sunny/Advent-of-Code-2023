from copy import deepcopy

Platform = list[list[str]]


def parse(input: str) -> Platform:
    platform = []

    for line in input.splitlines():
        platform.append([c for c in line])

    return platform


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


def compute_load(platform: Platform) -> int:
    load = 0

    n = len(platform)
    for i, line in enumerate(platform):
        load += sum(1 for c in line if c == "O") * (n - i)

    return load


def solve(input: str) -> int:
    platform = parse(input)
    platform = tilt_north(platform)

    return compute_load(platform)


if __name__ == "__main__":
    with open("./inputs/day14.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
