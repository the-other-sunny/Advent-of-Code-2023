import re
from dataclasses import dataclass
from typing_extensions import TypedDict


# defining a few types because type hinting >:3
class Outcome(TypedDict):
    red: int
    green: int
    blue: int


@dataclass
class Game:
    id: int
    outcomes: list[Outcome]


Bag = Outcome
# done with type definitions...

COLORS = ["red", "green", "blue"]


def parse_outcome(raw_outcome: str) -> Outcome:
    outcome: Outcome = {"red": 0, "green": 0, "blue": 0}

    for color_data in raw_outcome.split(", "):
        count, color = color_data.split()
        outcome[color] = int(count)  # type: ignore

    return outcome


def parse_game(line: str) -> Game:
    m = re.match(
        r"^Game (?P<game_id>\d+): (?P<game_outcomes>\d+ (red|green|blue)(, \d+ (red|green|blue))*(; \d+ (red|green|blue)(, \d+ (red|green|blue))*)*)$",
        line,
    )

    assert m is not None

    id = int(m["game_id"])
    outcomes_raw = m["game_outcomes"]
    outcomes = [parse_outcome(raw_outcome) for raw_outcome in outcomes_raw.split("; ")]

    return Game(id=id, outcomes=outcomes)


def outcome_is_possible(outcome: Outcome, bag_assumption: Bag) -> bool:
    return all(outcome[color] <= bag_assumption[color] for color in COLORS)  # type: ignore


def game_is_possible(game: Game, bag_assumption: Bag) -> bool:
    return all(
        outcome_is_possible(outcome, bag_assumption) for outcome in game.outcomes
    )


def solve(input: str, bag_assumption: Bag) -> int:
    games = [parse_game(line) for line in input.splitlines()]
    return sum(game.id for game in games if game_is_possible(game, bag_assumption))


if __name__ == "__main__":
    with open("./inputs/day2/input.txt", mode="r", encoding="utf-8") as file:
        input = file.read()

    bag_assumption: Bag = {"red": 12, "green": 13, "blue": 14}
    answer = solve(input, bag_assumption)
    print(f"{answer = }")
