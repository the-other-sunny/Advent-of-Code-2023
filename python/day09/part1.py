def parse(input) -> list[list[int]]:
    sequences = []

    for line in input.strip().splitlines():
        sequences.append([int(num_str) for num_str in line.split()])

    return sequences


def extrapolate(sequence: list[int]) -> int:
    result = 0

    diffs = sequence
    while not all(x == 0 for x in diffs):
        result += diffs[-1]
        diffs = [diffs[i + 1] - diffs[i] for i in range(len(diffs) - 1)]

    return result


def solve(input: str) -> int:
    sequences = parse(input)

    return sum(extrapolate(sequence) for sequence in sequences)


if __name__ == "__main__":
    with open("./inputs/day09.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer}")
