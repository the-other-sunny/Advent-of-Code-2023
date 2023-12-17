from enum import Enum
import re

TableEntry = tuple[int, int, int]


class TableNames(Enum):
    SEED_TO_SOIL = "seed-to-soil"
    SOIL_TO_FERTILIZER = "soil-to-fertilizer"
    FERTILIZER_TO_WATER = "fertilizer-to-water"
    WATER_TO_LIGHT = "water-to-light"
    LIGHT_TO_TEMPERATURE = "light-to-temperature"
    TEMPERATURE_TO_HUMIDITY = "temperature-to-humidity"
    HUMIDITY_TO_LOCATION = "humidity-to-location"


def parse(input: str) -> tuple[list[int], dict[TableNames, list[TableEntry]]]:
    def get_seeds(input: str) -> list[int]:
        m = re.search(r"^seeds:(?P<values>( \d+)*)$", input, flags=re.MULTILINE)

        assert m is not None

        return [int(s) for s in m["values"].split()]

    def get_table(table_name: TableNames, input: str) -> list[tuple[int, int, int]]:
        m = re.search(
            rf"^{table_name.value} map:\n(?P<lines>(\d+( \d+)*\n)*)",
            input,
            flags=re.MULTILINE,
        )

        assert m is not None

        return [
            tuple(int(num) for num in line.split())  # type: ignore
            for line in m["lines"].splitlines()
        ]

    return (
        get_seeds(input),
        {table_name: get_table(table_name, input) for table_name in TableNames},
    )


def convert_value(value: int, table_entries: list[TableEntry]) -> int:
    for d_start, s_start, length in table_entries:
        if s_start <= value < s_start + length:
            new_value = value + d_start - s_start

            return new_value

    return value


def solve(input: str) -> int:
    seeds, tables = parse(input)

    values = seeds
    for table_name in TableNames:
        values = [convert_value(value, tables[table_name]) for value in values]

    return min(values)


if __name__ == "__main__":
    with open("./inputs/day05.txt", encoding="utf-8") as file:
        input = file.read()

    answer = solve(input)
    print(f"{answer = }")
