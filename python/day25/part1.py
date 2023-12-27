import networkx as nx


def parse(input: str):
    G = nx.Graph()

    for line in input.splitlines():
        left, _, right = line.partition(": ")
        source = left
        dests = [node for node in right.split()]

        for dest in dests:
            G.add_edge(source, dest)

    return G


def solve(input: str) -> int:
    G = parse(input)

    # https://en.wikipedia.org/wiki/Stoer%E2%80%93Wagner_algorithm
    cut_value, partition = nx.stoer_wagner(G)

    assert cut_value == 3
    nodes_a, nodes_b = partition

    return len(nodes_a) * len(nodes_b)


if __name__ == "__main__":
    with open("./inputs/day25.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer}")
