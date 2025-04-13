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

        self.instructions = [
            self.instruction_adv,  # 0
            self.instruction_bxl,  # 1
            self.instruction_bst,  # 2
            self.instruction_jnz,  # 3
            self.instruction_bxc,  # 4
            self.instruction_out,  # 5
            self.instruction_bdv,  # 6
            self.instruction_cdv,  # 7
        ]

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

    def instruction_adv(self, operand: int):
        self.a = int(self.a / 2 ** self.combo(operand))
        self.ip += 2

    def instruction_bxl(self, operand: int):
        self.b ^= operand
        self.ip += 2

    def instruction_bst(self, operand: int):
        self.b = self.combo(operand) % 8
        self.ip += 2

    def instruction_jnz(self, operand: int):
        self.ip = operand if self.a != 0 else self.ip + 2

    def instruction_bxc(self, _: int):
        self.b ^= self.c
        self.ip += 2

    def instruction_out(self, operand: int):
        self.output.append(self.combo(operand) % 8)
        self.ip += 2

    def instruction_bdv(self, operand: int):
        self.b = int(self.a / 2 ** self.combo(operand))
        self.ip += 2

    def instruction_cdv(self, operand: int):
        self.c = int(self.a / 2 ** self.combo(operand))
        self.ip += 2

    def run(self) -> list[int]:
        while self.ip < len(self.program) - 1:
            op, operand = self.program[self.ip], self.program[self.ip + 1]
            self.instructions[op](operand)
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
    print(day17_part1(input_data))  # Correct answer is 2,0,7,3,0,3,1,3,7

    print("Day 17 Part 2:")
    print(day17_part2(input_data))  # Correct answer is 247839539763386
