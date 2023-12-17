def parse(input: str) -> list[str]:
    return input.split(",")


def hash_step(step: str) -> int:
    result = 0

    for c in step:
        result += ord(c)
        result *= 17
        result %= 256

    return result


def solve(input: str) -> int:
    steps = parse(input)

    return sum(hash_step(step) for step in steps)


if __name__ == "__main__":
    with open("./inputs/day15.txt", encoding="utf-8") as file:
        input = file.read().strip()

    answer = solve(input)
    print(f"{answer = }")
