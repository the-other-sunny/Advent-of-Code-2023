from typing import NamedTuple
import re


class Step(NamedTuple):
    label: str
    operation: str
    focal_length: int


def parse(input: str) -> list[Step]:
    steps = []

    for raw_step in input.split(","):
        m = re.fullmatch(r"(?P<label>\w+)(?P<operation>-|=)(?P<length>\d+)?", raw_step)
        assert m is not None

        steps.append(
            Step(
                m["label"],
                m["operation"],
                int(m["length"]) if m["length"] is not None else 0,
            )
        )

    return steps


def hash_label(label: str) -> int:
    result = 0

    for c in label:
        result += ord(c)
        result *= 17
        result %= 256

    return result


def solve(input: str) -> int:
    steps = parse(input)

    boxes: list[dict[str, int]] = [
        dict() for _ in range(256)  # dictionaries preserve key insertion order
    ]

    for step in steps:
        box = boxes[hash_label(step.label)]
        if step.operation == "=":
            box[step.label] = step.focal_length
        if step.operation == "-":
            if step.label in box:
                del box[step.label]

    total_focusing_power = 0
    for box_num, box in enumerate(boxes):
        for slot, focal_length in enumerate(box.values(), start=1):
            total_focusing_power += (box_num + 1) * slot * focal_length

    return total_focusing_power


if __name__ == "__main__":
    with open("./inputs/day15.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
