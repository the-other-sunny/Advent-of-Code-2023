from __future__ import annotations
from enum import Enum
from abc import ABC, abstractmethod
from queue import Queue
import re
from itertools import count
from math import lcm


class Pulse(Enum):
    Low = 0
    High = 1

    def opposite(self) -> Pulse:
        return Pulse(1 - self.value)


class Module(ABC):
    def __init__(self, name):
        self.name = name
        self.destinations = []

    def set_destinations(self, destinations: list[Module]) -> None:
        self.destinations = destinations.copy()

    def __hash__(self) -> int:
        return hash(self.name)

    @abstractmethod
    def process_input(self, source: Module, pulse: Pulse) -> list[tuple[Module, Pulse]]:
        ...


class Broadcaster(Module):
    def process_input(self, source: Module, pulse: Pulse) -> list[tuple[Module, Pulse]]:
        return [(dest, pulse) for dest in self.destinations]


class FlipFLop(Module):
    def __init__(self, name) -> None:
        super().__init__(name)

        self.state = False

    def process_input(self, source: Module, pulse: Pulse) -> list[tuple[Module, Pulse]]:
        if pulse == Pulse.High:
            return []

        self.state = not self.state

        out_pulse = Pulse.High if self.state else Pulse.Low

        return [(dest, out_pulse) for dest in self.destinations]


class Conjunction(Module):
    def __init__(self, name) -> None:
        super().__init__(name)

        self.state: dict[Module, Pulse] = {}

    def set_sources(self, sources: list[Module]) -> None:
        self.state = {module: Pulse.Low for module in sources}

    def add_source(self, source: Module) -> None:
        self.state[source] = Pulse.Low

    def process_input(self, source: Module, pulse: Pulse) -> list[tuple[Module, Pulse]]:
        self.state[source] = pulse

        out_pulse = (
            Pulse.Low
            if all(p == Pulse.High for p in self.state.values())
            else Pulse.High
        )

        return [(dest, out_pulse) for dest in self.destinations]


def parse(input: str) -> dict[str, Module]:
    modules: dict[str, Module] = {}

    destinations: dict[str, list[str]] = {}

    for line in input.splitlines():
        left, sep, right = line.partition(" -> ")

        m = re.match(r"^(?P<type>%|&|)(?P<name>\w+)$", left)
        assert m is not None

        dest_name = m["name"]

        match m["type"]:
            case "%":
                modules[dest_name] = FlipFLop(dest_name)
            case "&":
                modules[dest_name] = Conjunction(dest_name)
            case "":
                modules[dest_name] = Broadcaster(dest_name)
            case _:
                raise RuntimeError

        destinations[dest_name] = right.split(", ")

    for source_name, dest_names in destinations.items():
        source_module = modules[source_name]

        for dest_name in dest_names:
            # some modules are to be found in destinations but not in sources, we need to instantiate them
            if dest_name not in modules:
                modules[dest_name] = Broadcaster(dest_name)

            dest_module = modules[dest_name]
            if isinstance(dest_module, Conjunction):
                dest_module.add_source(source_module)

        source_module.set_destinations([modules[dest_name] for dest_name in dest_names])

    return modules


def get_cycle_length(in_module: Module, out_module: Module) -> int:
    for i in count(1):
        q: Queue[tuple[Module, Module, Pulse]] = Queue()
        q.put((Broadcaster(""), in_module, Pulse.Low))

        while not q.empty():
            source, dest, pulse = q.get()

            for next_dest, next_pulse in dest.process_input(source, pulse):
                if next_dest != out_module:
                    q.put((dest, next_dest, next_pulse))

                if next_dest == out_module and pulse == Pulse.Low:
                    return i

    raise RuntimeError


def solve(input: str) -> int:
    cycles_lengths = []

    for in_name in ["gb", "zz", "ht", "vk"]:
        modules = parse(input)

        in_module = modules[in_name]
        out_module = modules["mg"]

        cycles_lengths.append(get_cycle_length(in_module, out_module))

    return lcm(*cycles_lengths)


if __name__ == "__main__":
    with open("./inputs/day20.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)

    print(f"{answer = }")
