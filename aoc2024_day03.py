"""
Advent of Code 2024
Day 03: Mull It Over
"""

import re

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().strip()


def day03_part1(data):
    matches = re.findall(r"mul\((\d+),(\d+)\)", data)
    return sum(int(a) * int(b) for a, b in matches)


def day03_part2(data):
    matches = re.findall(r"(?:mul\((\d+),(\d+)\))|(do\(\)|don't\(\))", data)
    enabled = True
    total = 0
    for a, b, control in matches:
        if control:
            enabled = control == "do()"
        elif enabled:
            total += int(a) * int(b)
    return total


@pytest.fixture(name="test_data_part_1")
def fixture_test_data_part_1():
    return parse_input("data/day03_test_part1.txt")


@pytest.fixture(name="test_data_part_2")
def fixture_test_data_part_2():
    return parse_input("data/day03_test_part2.txt")


def test_day03_part1(test_data_part_1):
    assert day03_part1(test_data_part_1) == 161


def test_day03_part2(test_data_part_2):
    assert day03_part2(test_data_part_2) == 48


if __name__ == "__main__":
    input_data = parse_input("data/day03.txt")

    print("Day 03 Part 1:")
    print(day03_part1(input_data))

    print("Day 03 Part 2:")
    print(day03_part2(input_data))
