"""
Advent of Code 2024
Day 17: Chronospatial Computer
"""

import re


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        a, b, c, *program = map(int, re.findall(r"\d+", data_file.read()))
    return (a, b, c, program)


class Computer:
    def __init__(self, a: int, b: int, c: int, program: list[int]):
        self.a = a
        self.b = b
        self.c = c
        self.ip = 0
        self.output = []
        self.program = program

    def combo(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                raise ValueError(f"Invalid or reserved {operand=}.")

    def instruction(self, opcode: int, operand: int):
        match opcode:
            case 0:  # adv
                self.a = int(self.a / 2 ** self.combo(operand))
                self.ip += 2
            case 1:  # bxl
                self.b ^= operand
                self.ip += 2
            case 2:  # bst
                self.b = self.combo(operand) % 8
                self.ip += 2
            case 3:  # jnz
                self.ip = operand if self.a != 0 else self.ip + 2
            case 4:  # bxc
                self.b ^= self.c
                self.ip += 2
            case 5:  # out
                self.output.append(self.combo(operand) % 8)
                self.ip += 2
            case 6:  # bdv
                self.b = int(self.a / 2 ** self.combo(operand))
                self.ip += 2
            case 7:  # cdv
                self.c = int(self.a / 2 ** self.combo(operand))
                self.ip += 2
            case _:
                raise ValueError(f"Invalid opcode: {opcode}")

    def run(self) -> list[int]:
        while self.ip < len(self.program) - 1:
            opcode, operand = self.program[self.ip], self.program[self.ip + 1]
            self.instruction(opcode, operand)
        return self.output


def day17_part1(data):
    output = Computer(*data).run()
    return ",".join(str(x) for x in output)


def day17_part2(data):
    _, _, _, program = data
    stack = [(0, 0)]
    while stack:
        a, i = stack.pop()
        output = Computer(a, 0, 0, program).run()
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
    print(day17_part1(input_data))

    print("Day 17 Part 2:")
    print(day17_part2(input_data))
