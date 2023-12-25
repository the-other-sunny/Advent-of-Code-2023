import re
from typing import NamedTuple
from collections.abc import Callable
from enum import Enum, auto


class Status(Enum):
    ACCEPTED = auto()
    REJECTED = auto()


class Interval(NamedTuple):
    start: int
    end: int


DEFAULT_INTERVAL = Interval(1, 4001)


class PartsRange(NamedTuple):
    x: Interval = DEFAULT_INTERVAL
    m: Interval = DEFAULT_INTERVAL
    a: Interval = DEFAULT_INTERVAL
    s: Interval = DEFAULT_INTERVAL

    def get_count(self) -> int:
        return (
            (self.x.end - self.x.start)
            * (self.m.end - self.m.start)
            * (self.a.end - self.a.start)
            * (self.s.end - self.s.start)
        )


class ConditionResult(NamedTuple):
    accepted: PartsRange | None
    rejected: PartsRange | None


class Condition(NamedTuple):
    check: Callable[[PartsRange], ConditionResult]
    dest: str


class WorkflowResult(NamedTuple):
    accepted: set[PartsRange] = set()
    rejected: set[PartsRange] = set()


Workflow = Callable[[PartsRange, WorkflowResult], None]


def workflow_A(parts_range: PartsRange, result: WorkflowResult):
    result.accepted.add(parts_range)


def workflow_R(parts_range: PartsRange, result: WorkflowResult):
    result.rejected.add(parts_range)


def make_workflow(
    conditions: list[Condition], workflows: dict[str, Workflow]
) -> Workflow:
    def workflow(parts_range: PartsRange, result: WorkflowResult):
        remaining_range: PartsRange | None = parts_range
        for condition in conditions:
            if remaining_range is None:
                break

            accepted_range, remaining_range = condition.check(remaining_range)

            if accepted_range:
                workflows[condition.dest](accepted_range, result)

    return workflow


def make_condition(condition_str: str) -> Condition:
    def make_check(cat, cmp, value):
        def check(parts_range: PartsRange) -> ConditionResult:
            a, r = None, None
            i: Interval = getattr(parts_range, cat)

            if cmp == "<":
                if value <= i.start:
                    a, r = None, i
                elif i.end <= value:
                    a, r = i, None
                else:
                    a, r = Interval(i.start, value), Interval(value, i.end)

            if cmp == ">":
                if value + 1 <= i.start:
                    a, r = i, None
                elif i.end <= value + 1:
                    a, r = None, i
                else:
                    a, r = Interval(value + 1, i.end), Interval(i.start, value + 1)

            accepted_range = None if a is None else parts_range._replace(**{cat: a})
            rejected_range = None if r is None else parts_range._replace(**{cat: r})

            return ConditionResult(accepted_range, rejected_range)

        return check

    m = re.fullmatch(r"([xmas])([<>])(\d+):([AR]|[a-z]+)", condition_str)

    if m is not None:
        cat = m[1]
        cmp = m[2]
        value = int(m[3])
        dest = m[4]

        return Condition(make_check(cat, cmp, value), dest)

    m = re.fullmatch(r"([AR]|[a-z]+)", condition_str)

    if m is not None:
        dest = m[1]

        return Condition(lambda parts_range: ConditionResult(parts_range, None), dest)

    raise ValueError


def parse(input: str) -> dict[str, Workflow]:
    workflows: dict[str, Workflow] = {}

    workflows_str, _ = input.split("\n\n")

    workflows["A"] = workflow_A
    workflows["R"] = workflow_R

    for raw_workflow in workflows_str.splitlines():
        m = re.fullmatch(r"([a-z]+){(.*)}", raw_workflow)

        assert m is not None

        id = m[1]
        conditions_strings = m[2].split(",")
        conditions = [make_condition(s) for s in conditions_strings]

        workflows[id] = make_workflow(conditions, workflows)

    return workflows


def solve(input: str) -> int:
    workflows = parse(input)

    parts_range = PartsRange()
    result = WorkflowResult()
    workflows["in"](parts_range, result)

    answer = 0

    for parts_range in result.accepted:
        answer += (
            (parts_range.x.end - parts_range.x.start)
            * (parts_range.m.end - parts_range.m.start)
            * (parts_range.a.end - parts_range.a.start)
            * (parts_range.s.end - parts_range.s.start)
        )

    return answer


if __name__ == "__main__":
    with open("./inputs/day19.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
