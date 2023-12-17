def parse(input: str) -> tuple[int, int]:
    lines = input.splitlines()

    time = int(lines[0].removeprefix("Time:").replace(" ", ""))
    distance = int(lines[1].removeprefix("Distance:").replace(" ", ""))

    return time, distance


def solve(input: str) -> int:
    time, distance = parse(input)
    # too lazy for solving a quadratic equation...
    wins = 0
    for charge_time in range(time + 1):
        distance_traveled = (time - charge_time) * charge_time
        if distance_traveled > distance:
            wins += 1

    return wins


if __name__ == "__main__":
    with open("./inputs/day06.txt", mode="r", encoding="utf-8") as file:
        input = file.read()

    answer = solve(input)
    print(f"{answer = }")
