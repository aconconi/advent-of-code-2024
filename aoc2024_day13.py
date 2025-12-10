"""
Advent of Code 2024
Day 13: Claw Contraption
"""

import re

import numpy as np
import pytest


def parse_input(file_name: str) -> list[tuple[np.ndarray, np.ndarray]]:
    def parse_machine(lines: str) -> tuple[np.ndarray, np.ndarray]:
        matrix = [
            [int(x) for x in re.findall(r"\d+", line)] for line in lines.splitlines()
        ]
        return np.transpose(matrix[:2]), np.array(matrix[2])

    with open(file_name, "r", encoding="ascii") as data_file:
        return [
            parse_machine(three_lines) for three_lines in data_file.read().split("\n\n")
        ]


def solve_machine(machine: tuple[np.ndarray, np.ndarray], offset: int = 0) -> int:
    coefficients_matrix, constant_vector = machine
    if offset:
        constant_vector = constant_vector + offset  # avoid mutating input
    variables = np.linalg.solve(coefficients_matrix, constant_vector)
    rounded = np.rint(variables).astype(int)
    if np.array_equal(coefficients_matrix @ rounded, constant_vector):
        na, nb = rounded
        return 3 * na + nb
    return 0


def day13_part1(data: list[tuple[np.ndarray, np.ndarray]]) -> int:
    return sum(solve_machine(machine) for machine in data)


def day13_part2(data: list[tuple[np.ndarray, np.ndarray]]) -> int:
    return sum(solve_machine(machine, offset=10_000_000_000_000) for machine in data)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day13_test.txt")


def test_day13_part1(test_data):
    assert day13_part1(test_data) == 480


def test_day13_part2(test_data):
    assert day13_part2(test_data) == 875_318_608_908


if __name__ == "__main__":
    input_data = parse_input("data/day13.txt")

    print("Day 13 Part 1:")
    print(day13_part1(input_data))

    print("Day 13 Part 2:")
    print(day13_part2(input_data))
