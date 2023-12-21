from __future__ import annotations
from enum import Enum
from abc import ABC, abstractmethod
import re

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


def get_graph_data(modules: dict[str, Module]):
    nodes = []
    edges = []

    for module in modules.values():
        match module:
            case Broadcaster():
                color = "0,255,0"
            case FlipFLop():
                color = "0,0,255"
            case Conjunction():
                color = "255,0,0"
            case _:
                raise RuntimeError

        nodes.append({"Id": module.name, "Label": module.name, "Color": color})
        
        for dest in module.destinations:
            edges.append({"Source": module.name, "Target": dest.name})
    
    return nodes, edges


if __name__ == "__main__":
    import csv
    
    with open("./inputs/day20.txt", encoding="utf-8") as file:
        input = file.read().strip()

    modules = parse(input)
    nodes, edges = get_graph_data(modules)
    
    with open("./python/day20/graph/nodes.csv", mode="w", newline='', encoding='utf-8') as nodes_file:
        writer = csv.DictWriter(nodes_file, fieldnames=["Id", "Label", "Color"])
        
        writer.writeheader()
        writer.writerows(nodes)

    with open("./python/day20/graph/edges.csv", mode="w", newline='', encoding='utf-8') as edges_file:
        writer = csv.DictWriter(edges_file, fieldnames=["Source", "Target"])
        
        writer.writeheader()
        writer.writerows(edges)
    
    print("Done!")
