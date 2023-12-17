from collections import defaultdict
from collections.abc import Iterator
from itertools import product


def parse(input: str) -> list[tuple[str, tuple[int, ...]]]:
    result = []

    for line in input.splitlines():
        incomplete_springs_row, groups_str = line.split()
        groups = tuple(int(c) for c in groups_str.split(","))

        result.append((incomplete_springs_row, groups))

    return result


def expand_row(spring: str) -> str:
    return "?".join(spring for _ in range(5))


def expand_groups(groups: tuple[int, ...]) -> tuple[int, ...]:
    return 5 * groups


def valid_springs_rows_count(springs_row: str, groups: tuple[int, ...]) -> int:
    def get_groups_iter(groups: tuple[int, ...]) -> Iterator[tuple[int, ...]]:
        yield ()
        for i in range(len(groups)):
            for k in range(1, groups[i] + 1):
                yield (*groups[:i], k)

    # dynamic programming: counts the number of candidate rows for a given state
    # a state is:
    # - a prefix of springs_row
    # - a tuple lower than `groups` (using lexico order)
    # - a boolean indicating if we're counting the candidate rows ending with a "." or a "#"
    dp: dict[tuple[str, tuple[int, ...], bool], int] = defaultdict(int)

    # initialization
    dp[("", (), True)] = 1

    springs_iter = iter([springs_row[:i] for i in range(1, len(springs_row) + 1)])
    groups_iter = get_groups_iter(groups)

    for s, g in product(springs_iter, groups_iter):
        prev_s = s[:-1]

        if s[-1] == "." or s[-1] == "?":
            dp[(s, g, True)] = dp[(prev_s, g, True)] + dp[(prev_s, g, False)]

        if s[-1] == "#" or s[-1] == "?":
            if len(g) > 0 and g[-1] == 1:
                dp[(s, g, False)] = dp[(prev_s, g[:-1], True)]

            if len(g) > 0 and g[-1] > 1:
                prev_g = (*g[:-1], g[-1] - 1)
                dp[(s, g, False)] = dp[(prev_s, prev_g, False)]

    count = dp[(springs_row, groups, True)] + dp[(springs_row, groups, False)]

    return count


def solve(input: str) -> int:
    answer = 0

    for incomplete_springs_row, groups in parse(input):
        answer += valid_springs_rows_count(
            expand_row(incomplete_springs_row), expand_groups(groups)
        )

    return answer


if __name__ == "__main__":
    with open("./inputs/day12.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
