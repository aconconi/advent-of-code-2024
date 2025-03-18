"""
Advent of Code 2024
Day 07: Bridge Repair
"""

import operator
from itertools import product

import pytest


def parse_input(file_name):
    def process_line(line):
        result, numbers = line.split(":")
        return (int(result), [int(num) for num in numbers.split()])

    with open(file_name, "r", encoding="ascii") as data_file:
        return [process_line(line) for line in data_file.read().splitlines()]


def evaluate(numbers, operators):
    result = numbers[0]
    for num, op in zip(numbers[1:], operators):
        result = op(result, num)
    return result


def find_operators(result, numbers, possible_operators):
    return next(
        (
            operators
            for operators in product(possible_operators, repeat=len(numbers) - 1)
            if evaluate(numbers, operators) == result
        ),
        None,
    )


def solve(data, possible_operators):
    return sum(
        result
        for result, numbers in data
        if find_operators(result, numbers, possible_operators) is not None
    )


def day07_part1(data):
    possible_operators = [operator.add, operator.mul]
    return solve(data, possible_operators)


def day07_part2(data):
    possible_operators = [operator.add, operator.mul, lambda x, y: int(str(x) + str(y))]
    return solve(data, possible_operators)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day07_test.txt")


def test_day07_part1(test_data):
    assert day07_part1(test_data) == 3749


def test_day07_part2(test_data):
    assert day07_part2(test_data) == 11387


if __name__ == "__main__":
    input_data = parse_input("data/day07.txt")

    print("Day 07 Part 1:")
    print(day07_part1(input_data))  # Correct answer is 5_837_374_519_342

    print("Day 07 Part 2:")
    print(day07_part2(input_data))  # Correct answer is 492_383_931_650_959
