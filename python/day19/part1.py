import re
from typing import NamedTuple
import operator
from collections.abc import Callable
from enum import Enum, auto


class Status(Enum):
    ACCEPTED = auto()
    REJECTED = auto()


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int


class Condition(NamedTuple):
    check: Callable[[Part], bool]
    dest: str


Workflow = Callable[[Part], Status]


def make_workflow(
    conditions: list[Condition], workflows: dict[str, Workflow]
) -> Workflow:
    def workflow(part: Part) -> Status:
        for condition in conditions:
            if condition.check(part):
                return workflows[condition.dest](part)

        raise RuntimeError("No condition met")

    return workflow


def make_condition(condition_str: str) -> Condition:
    def make_check(cat, cmp, value):
        def check(part: Part) -> bool:
            part_value = getattr(part, cat)
            return cmp(part_value, value)

        return check

    m = re.fullmatch(r"([xmas])([<>])(\d+):([AR]|[a-z]+)", condition_str)

    if m is not None:
        cat = m[1]
        cmp = operator.lt if m[2] == "<" else operator.gt
        value = int(m[3])
        dest = m[4]

        return Condition(make_check(cat, cmp, value), dest)

    m = re.fullmatch(r"([AR]|[a-z]+)", condition_str)

    if m is not None:
        dest = m[1]

        return Condition(lambda _: True, dest)

    raise ValueError


def parse(input: str) -> tuple[dict[str, Workflow], list[Part]]:
    workflows: dict[str, Workflow] = {}
    parts: list[Part] = []

    workflows_str, parts_str = input.split("\n\n")

    workflows["A"] = lambda _: Status.ACCEPTED
    workflows["R"] = lambda _: Status.REJECTED

    for raw_workflow in workflows_str.splitlines():
        m = re.fullmatch(r"([a-z]+)\{(.*)\}", raw_workflow)

        assert m is not None

        id = m[1]
        conditions_strings = m[2].split(",")
        conditions = [make_condition(s) for s in conditions_strings]

        workflows[id] = make_workflow(conditions, workflows)

    for raw_part in parts_str.splitlines():
        m = re.fullmatch(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", raw_part)

        assert m is not None

        part = Part(x=int(m[1]), m=int(m[2]), a=int(m[3]), s=int(m[4]))
        parts.append(part)

    return workflows, parts


def solve(input: str) -> int:
    workflows, parts = parse(input)

    answer = 0

    for part in parts:
        status = workflows["in"](part)
        if status is Status.ACCEPTED:
            answer += part.x + part.m + part.a + part.s

    return answer


if __name__ == "__main__":
    with open("./inputs/day19.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
