"""
Advent of Code 2024
Day 24: Crossed Wires
"""

from dataclasses import dataclass

import pytest


@dataclass
class Gate:
    input1: str
    input2: str
    op: str
    output: str

    def __hash__(self) -> int:
        return hash((self.input1, self.input2, self.op, self.output))

    def is_to_be_solved(self, wires: dict[str, bool]) -> bool:
        return (
            self.input1 in wires and self.input2 in wires and self.output not in wires
        )

    def compute(self, wires: dict[str, bool]) -> None:
        x, y = wires[self.input1], wires[self.input2]
        match self.op:
            case "AND":
                wires[self.output] = x and y
            case "OR":
                wires[self.output] = x or y
            case "XOR":
                wires[self.output] = x ^ y

    @classmethod
    def from_line(cls, line: str) -> "Gate":
        tokens = line.split(" ")
        return Gate(input1=tokens[0], op=tokens[1], input2=tokens[2], output=tokens[4])


def parse_input(file_name: str) -> tuple[dict[str, bool], list[Gate]]:
    with open(file_name, "r", encoding="ascii") as data_file:
        wires, gates = map(str.splitlines, data_file.read().split("\n\n"))
    wires = {w[:3]: bool(int(w[-1])) for w in wires}
    gates = [Gate.from_line(line) for line in gates]
    return wires, gates


def day24_part1(data: tuple[dict[str, bool], list[Gate]]) -> int:
    initial_wires, gates = data
    wires = dict(initial_wires)
    while solvable := {g for g in gates if g.is_to_be_solved(wires)}:
        for g in solvable:
            g.compute(wires)

    digits = [
        int(wire_value)
        for wire_label, wire_value in sorted(wires.items())
        if wire_label.startswith("z")
    ]
    return sum(digit * 2**i for i, digit in enumerate(digits))


def day24_part2(data: tuple[dict[str, bool], list[Gate]]) -> str:
    _, gates = data

    carry_wire = max(g.output for g in gates if g.output.startswith("z"))

    def check_gate_op_and_inputs(v: str, op: str) -> bool:
        return any(g.op == op and v in (g.input1, g.input2) for g in gates)

    def is_wrong_gate(g: Gate) -> bool:
        is_xor_with_non_xyz = g.op == "XOR" and all(
            wire[0] not in "xyz" for wire in (g.input1, g.input2, g.output)
        )
        is_and_without_x00_and_xor_output = (
            g.op == "AND"
            and "x00" not in (g.input1, g.input2)
            and check_gate_op_and_inputs(g.output, "XOR")
        )
        is_xor_without_x00_and_or_output = (
            g.op == "XOR"
            and "x00" not in (g.input1, g.input2)
            and check_gate_op_and_inputs(g.output, "OR")
        )
        is_non_xor_with_wrong_z_output = (
            g.op != "XOR" and g.output[0] == "z" and g.output != carry_wire
        )

        return any(
            [
                is_xor_with_non_xyz,
                is_and_without_x00_and_xor_output,
                is_xor_without_x00_and_or_output,
                is_non_xor_with_wrong_z_output,
            ]
        )

    wrong_outputs = set(g.output for g in gates if is_wrong_gate(g))
    return ",".join(sorted(wrong_outputs))


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data() -> tuple[dict[str, bool], list[Gate]]:
    return parse_input("data/day24_test.txt")


def test_day24_part1(test_data: tuple[dict[str, bool], list[Gate]]) -> None:
    assert day24_part1(test_data) == 2024


def test_day24_part2(test_data: tuple[dict[str, bool], list[Gate]]) -> None:
    assert (
        day24_part2(test_data) == "ffh,mjb,rvg,tgd,wpb,z02,z03,z05,z06,z07,z08,z10,z11"
    )


if __name__ == "__main__":
    input_data = parse_input("data/day24.txt")

    print("Day 24 Part 1:")
    print(day24_part1(input_data))

    print("Day 24 Part 2:")
    print(day24_part2(input_data))
