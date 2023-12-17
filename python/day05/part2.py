from __future__ import annotations
from enum import Enum
import re
from typing import NamedTuple
from collections.abc import Callable


class TableName(Enum):
    SEED_TO_SOIL = "seed-to-soil"
    SOIL_TO_FERTILIZER = "soil-to-fertilizer"
    FERTILIZER_TO_WATER = "fertilizer-to-water"
    WATER_TO_LIGHT = "water-to-light"
    LIGHT_TO_TEMPERATURE = "light-to-temperature"
    TEMPERATURE_TO_HUMIDITY = "temperature-to-humidity"
    HUMIDITY_TO_LOCATION = "humidity-to-location"


TableEntry = tuple[int, int, int]
TableData = list[TableEntry]
Tables = dict[TableName, TableData]
MappingFn = Callable[[int], int]


class Interval(NamedTuple):
    start: int
    end: int

    def intersection(self: Interval, other: Interval) -> Interval | None:
        intersection_start = max(self.start, other.start)
        intersection_end = min(self.end, other.end)

        if intersection_start > intersection_end:
            return None

        return Interval(intersection_start, intersection_end)

    def substract(self, other: Interval) -> list[Interval]:
        result = []

        if other.start > self.start:
            start = self.start
            end = min(self.end, other.start - 1)
            result.append(Interval(start, end))

        if other.end < self.end:
            start = max(self.start, other.end + 1)
            end = self.end
            result.append(Interval(start, end))

        return result


def parse(input: str) -> tuple[list[Interval], Tables]:
    def get_seeds(input: str) -> list[Interval]:
        m = re.match(r"seeds:(?P<values>( \d+)*)\n", input)

        assert m is not None

        values = [int(s) for s in m["values"].split()]

        return [
            Interval(start, start + length - 1)
            for start, length in zip(values[::2], values[1::2])
        ]

    def get_table(table_name: TableName, input: str) -> list[tuple[int, int, int]]:
        m = re.search(
            rf"^{table_name.value} map:\n(?P<lines>(\d+( \d+)*\n)*)",
            input,
            flags=re.MULTILINE,
        )

        assert m is not None

        return sorted(
            tuple(int(num) for num in line.split()) for line in m["lines"].splitlines()  # type: ignore
        )

    def get_tables(input: str) -> Tables:
        return {table_name: get_table(table_name, input) for table_name in TableName}

    return get_seeds(input), get_tables(input)


def convert_interval(interval: Interval, convertion_table: TableData) -> list[Interval]:
    new_intervals = []

    leftovers = [interval]
    for d_start, s_start, length in convertion_table:
        offset = d_start - s_start
        source_interval = Interval(s_start, s_start + length - 1)

        leftovers_ = []

        for i in leftovers:
            if intersection := i.intersection(source_interval):
                leftovers_.extend(i.substract(intersection))
                new_interval = Interval(
                    intersection.start + offset, intersection.end + offset
                )
                new_intervals.append(new_interval)
            else:
                leftovers_.append(i)

        leftovers = leftovers_

    return new_intervals + leftovers


def convert_intervals(
    intervals: list[Interval], convertion_table: TableData
) -> list[Interval]:
    new_intervals = []

    for interval in intervals:
        new_intervals.extend(convert_interval(interval, convertion_table))

    return new_intervals


def solve(input: str) -> int:
    intervals, tables = parse(input)

    for table_name in TableName:
        intervals = convert_intervals(intervals, tables[table_name])

    return min(interval.start for interval in intervals)


if __name__ == "__main__":
    with open("./inputs/day05.txt", mode="r", encoding="utf-8") as file:
        input = file.read()

    answer = solve(input)
    print(f"{answer = }")
