from collections import defaultdict
from enum import Enum
from functools import cache


class HandType(Enum):
    FIVE_OF_A_KIND = -1
    FOUR_OF_A_KIND = -2
    FULL_HOUSE = -3
    THREE_OF_A_KIND = -4
    TWO_PAIRS = -5
    ONE_PAIR = -6
    HIGH_CARD = -7


@cache
def get_card_strength(card: str) -> int:
    ordered_cards = list(
        reversed(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"])
    )
    return ordered_cards.index(card)


def get_cards_counts(hand: str) -> dict[str, int]:
    counts: defaultdict[str, int] = defaultdict(int)

    for card in hand:
        counts[card] += 1

    return dict(counts)


def get_hand_type(hand: str) -> HandType:
    cards_counts = get_cards_counts(hand)

    match sorted(cards_counts.values()):
        case [5]:
            return HandType.FIVE_OF_A_KIND
        case [1, 4]:
            return HandType.FOUR_OF_A_KIND
        case [2, 3]:
            return HandType.FULL_HOUSE
        case [1, 1, 3]:
            return HandType.THREE_OF_A_KIND
        case [1, 2, 2]:
            return HandType.TWO_PAIRS
        case [1, 1, 1, 2]:
            return HandType.ONE_PAIR
        case [1, 1, 1, 1, 1]:
            return HandType.HIGH_CARD
        case _:
            raise RuntimeError


def hand_comparison_key(hand: str) -> tuple[int, tuple[int, ...]]:
    return get_hand_type(hand).value, tuple(get_card_strength(card) for card in hand)


def parse(input: str) -> list[tuple[str, int]]:
    hands = []

    for line in input.splitlines():
        hand, bid_str = line.split()
        bid = int(bid_str)
        hand = hand

        hands.append((hand, bid))

    return hands


def solve(input: str) -> int:
    hands = parse(input)
    sorted_hands = sorted(hands, key=lambda x: hand_comparison_key(x[0]))

    winnings = 0
    for rank, (hand, bid) in enumerate(sorted_hands, start=1):
        winnings += rank * bid

    return winnings


if __name__ == "__main__":
    with open("./inputs/day07.txt", encoding="utf-8") as file:
        input = file.read()

    answer = solve(input)
    print(f"{answer = }")
