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


def minimal_bag(game: Game) -> Bag:
    min_bag: Bag = {"red": 0, "green": 0, "blue": 0}
    for color in COLORS:
        min_bag[color] = max(  # type: ignore
            (outcome[color] for outcome in game.outcomes), default=0  # type: ignore
        )
    return min_bag


def power(min_bag: Bag) -> int:
    return min_bag["red"] * min_bag["green"] * min_bag["blue"]


def solve(input: str) -> int:
    games = [parse_game(line) for line in input.splitlines()]
    return sum(power(minimal_bag(game)) for game in games)


if __name__ == "__main__":
    with open("./inputs/day2/input.txt", mode="r", encoding="utf-8") as file:
        input = file.read()

    answer = solve(input)
    print(f"{answer = }")
