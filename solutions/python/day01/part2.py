from itertools import product

WORD_TOKENS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
DIGIT_TOKENS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
TOKENS = DIGIT_TOKENS + WORD_TOKENS


def token_to_digit(token: str) -> int:
    if len(token) == 1 and token[0].isdigit():
        return int(token[0])
    else:
        return WORD_TOKENS.index(token) + 1


def get_tokens(line: str) -> list[str]:
    # some digits can be overlapping, like `oneight`...
    tokens = []
    for i, token in product(range(len(line)), TOKENS):
        if line[i:].startswith(token):
            tokens.append(token)
    return tokens


def solve(input: str) -> int:
    total = 0

    for line in input.splitlines(keepends=False):
        digits = [token_to_digit(token) for token in get_tokens(line)]
        line_value = 10 * digits[0] + digits[-1]
        total += line_value

    return total


if __name__ == "__main__":
    with open("./inputs/day01.txt", mode="r", encoding="utf-8") as file:
        input = file.read()

    answer = solve(input)
    print(f"{answer = }")
