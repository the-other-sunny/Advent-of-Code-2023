Pattern = list[list[str]]


def parse(input: str) -> list[Pattern]:
    patterns = []

    for pattern_str in input.split("\n\n"):
        pattern = [[c for c in line] for line in pattern_str.splitlines()]
        patterns.append(pattern)

    return patterns


def transpose(pattern: Pattern) -> Pattern:
    lines_count, cols_count = len(pattern), len(pattern[0])
    return [[pattern[i][j] for i in range(lines_count)] for j in range(cols_count)]


def get_horizontal_symetries(pattern: Pattern) -> list[tuple[int, int]]:
    syms = []

    lines_count = len(pattern)
    for i in range(lines_count - 1):
        t_iter = reversed(range(i + 1))  # i, i-1, ..., 0
        b_iter = range(i + 1, lines_count)  # i+1, i+2, ..., lines_count-1
        if all(pattern[t] == pattern[b] for (t, b) in zip(t_iter, b_iter)):
            syms.append((i, i + 1))

    return syms


def find_symetries(
    pattern: Pattern,
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    horizontal_syms = get_horizontal_symetries(pattern)
    vertical_syms = get_horizontal_symetries(transpose(pattern))

    return vertical_syms, horizontal_syms


def solve(input: str) -> int:
    answer = 0

    for pattern in parse(input):
        vertical_syms, horizontal_syms = find_symetries(pattern)

        assert len(vertical_syms) + len(horizontal_syms) == 1

        for left_index, right_index in vertical_syms:
            answer += left_index + 1

        for top_index, bottom_index in horizontal_syms:
            answer += 100 * (top_index + 1)

    return answer


if __name__ == "__main__":
    with open("./inputs/day13.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
