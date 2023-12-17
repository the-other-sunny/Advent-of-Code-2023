import re


def parse(input: str) -> list[tuple[str, tuple[int, ...]]]:
    result = []

    for line in input.splitlines():
        incomplete_springs_row, groups_str = line.split()
        groups = tuple(int(c) for c in groups_str.split(","))

        result.append((incomplete_springs_row, groups))

    return result


# good dumb and slow brute-force yaay!
def bf_springs(springs_row: str) -> list[str]:
    def recursive_bf(
        springs_row: list[str], start_i: int, collected_data: list[str]
    ) -> None:
        n = len(springs_row)

        for i in range(start_i, n):
            if springs_row[i] != "?":
                continue

            springs_row[i] = "."
            recursive_bf(springs_row, i + 1, collected_data)

            springs_row[i] = "#"
            recursive_bf(springs_row, i + 1, collected_data)

            springs_row[i] = "?"

            return

        collected_data.append("".join(springs_row))

    possible_springs: list[str] = []
    recursive_bf(list(springs_row), 0, possible_springs)

    return possible_springs


def compute_groups(springs_row: str) -> tuple[int, ...]:
    return tuple(len(m) for m in re.findall("#+", springs_row))


def valid_springs_rows_count(springs_row: str, groups: tuple[int, ...]) -> int:
    return len(
        [
            possible_springs_row
            for possible_springs_row in bf_springs(springs_row)
            if compute_groups(possible_springs_row) == groups
        ]
    )


def solve(input: str) -> int:
    answer = 0

    for springs_row, groups in parse(input):
        answer += valid_springs_rows_count(springs_row, groups)

    return answer


if __name__ == "__main__":
    with open("./inputs/day12.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
