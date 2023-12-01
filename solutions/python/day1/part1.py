def solve(input: str) -> int:
    total = 0

    for line in input.splitlines(keepends=False):
        digits = [int(c) for c in line if c.isdigit()]
        line_value = 10*digits[0] + digits[-1]
        total += line_value

    return total


if __name__ == '__main__':
    with open('./inputs/1/input.txt', mode='r', encoding='utf-8') as file:
        input = file.read()
    
    answer = solve(input)
    print(f'{answer = }')
