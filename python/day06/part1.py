def parse(input: str) -> tuple[list[int], list[int]]:
    lines = input.splitlines()

    times = [int(t_str) for t_str in lines[0].removeprefix("Time:").split()]
    distances = [int(d_str) for d_str in lines[1].removeprefix("Distance:").split()]

    return times, distances


def solve(input: str) -> int:
    times, distances = parse(input)

    answer = 1

    for time, distance in zip(times, distances):
        wins = 0

        for charge_time in range(time + 1):
            distance_traveled = (time - charge_time) * charge_time
            if distance_traveled > distance:
                wins += 1

        answer *= wins

    return answer


if __name__ == "__main__":
    with open("./inputs/day06.txt", mode="r", encoding="utf-8") as file:
        input = file.read()

    answer = solve(input)
    print(f"{answer = }")
