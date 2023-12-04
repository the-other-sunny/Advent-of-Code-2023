import re
from dataclasses import dataclass

REGEX = re.compile(
    r"^Card\s+\d+:(?P<winning_numbers>(\s+\d+)*) \|(?P<obtained_numbers>(\s+\d+)*)$"
)


@dataclass
class CardData:
    matches_count: int = 0
    copies: int = 1


def parse_line(line: str) -> tuple[list[int], list[int]]:
    m = REGEX.match(line)
    assert m is not None

    winning_numbers = [
        int(number_string) for number_string in m["winning_numbers"].split()
    ]

    obtained_numbers = [
        int(number_string) for number_string in m["obtained_numbers"].split()
    ]

    return winning_numbers, obtained_numbers


def count_matches(winning_numbers: list[int], obtained_numbers: list[int]) -> int:
    winning_numbers_ = set(winning_numbers)
    return sum(1 for number in obtained_numbers if number in winning_numbers_)


def solve(input: str) -> int:
    cards_data: list[CardData] = []
    for i, line in enumerate(input.splitlines()):
        winning_numbers, obtained_numbers = parse_line(line)
        matches_count = count_matches(winning_numbers, obtained_numbers)
        cards_data.append(CardData(matches_count, copies=1))

    # update copies counts
    for i, card_data in enumerate(cards_data):
        matches_count = card_data.matches_count
        # update next cards
        for j in range(i + 1, i + 1 + matches_count):
            cards_data[j].copies += card_data.copies

    answer = sum(line_data.copies for line_data in cards_data)

    return answer


if __name__ == "__main__":
    with open("./inputs/day4/input.txt", mode="r", encoding="utf-8") as file:
        input = file.read()

    answer = solve(input)
    print(f"{answer = }")
