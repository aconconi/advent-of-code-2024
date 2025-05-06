"""
Advent of Code 2024
Day 17: Chronospatial Computer
"""

import re


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        a, b, c, *program = map(int, re.findall(r"\d+", data_file.read()))
    return (a, b, c, program)


def combo(operand: int, a: int, b: int, c: int) -> int:
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return a
        case 5:
            return b
        case 6:
            return c
        case _:
            raise ValueError(f"Invalid or reserved {operand=}.")


def instruction_adv(operand, a, b, c, ip, output):
    a = int(a / 2 ** combo(operand, a, b, c))
    ip += 2
    return a, b, c, ip, output


def instruction_bxl(operand, a, b, c, ip, output):
    b ^= operand
    ip += 2
    return a, b, c, ip, output


def instruction_bst(operand, a, b, c, ip, output):
    b = combo(operand, a, b, c) % 8
    ip += 2
    return a, b, c, ip, output


def instruction_jnz(operand, a, b, c, ip, output):
    ip = operand if a != 0 else ip + 2
    return a, b, c, ip, output


def instruction_bxc(operand, a, b, c, ip, output):
    b ^= c
    ip += 2
    return a, b, c, ip, output


def instruction_out(operand, a, b, c, ip, output):
    output = output + [combo(operand, a, b, c) % 8]
    ip += 2
    return a, b, c, ip, output


def instruction_bdv(operand, a, b, c, ip, output):
    b = int(a / 2 ** combo(operand, a, b, c))
    ip += 2
    return a, b, c, ip, output


def instruction_cdv(operand, a, b, c, ip, output):
    c = int(a / 2 ** combo(operand, a, b, c))
    ip += 2
    return a, b, c, ip, output


INSTRUCTIONS = [
    instruction_adv,  # 0
    instruction_bxl,  # 1
    instruction_bst,  # 2
    instruction_jnz,  # 3
    instruction_bxc,  # 4
    instruction_out,  # 5
    instruction_bdv,  # 6
    instruction_cdv,  # 7
]


def compute(a, b, c, program):
    ip = 0
    output = []
    while ip < len(program) - 1:
        opcode, operand = program[ip], program[ip + 1]
        a, b, c, ip, output = INSTRUCTIONS[opcode](operand, a, b, c, ip, output)
    return output


def day17_part1(data):
    output = compute(*data)
    return ",".join(str(x) for x in output)


def day17_part2(data):
    *_, program = data
    stack = [(0, 0)]
    while stack:
        a, i = stack.pop()
        output = compute(a, 0, 0, program)
        if output == program:
            return a
        if output == program[-i:] or i == 0:
            stack.extend((8 * a + n, i + 1) for n in reversed(range(8)))
    return None


def test_day17_part1():
    test_data_1 = parse_input("data/day17_test.txt")
    assert day17_part1(test_data_1) == "4,6,3,5,6,3,5,2,1,0"


def test_day17_part2():
    test_data_2 = parse_input("data/day17_test2.txt")
    assert day17_part2(test_data_2) == 117440


if __name__ == "__main__":
    input_data = parse_input("data/day17.txt")

    print("Day 17 Part 1:")
    print(day17_part1(input_data))  # Correct answer is 2,0,7,3,0,3,1,3,7

    print("Day 17 Part 2:")
    print(day17_part2(input_data))  # Correct answer is 247839539763386
