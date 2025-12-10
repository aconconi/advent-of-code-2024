"""
Advent of Code 2024
Day 01: Historian Hysteria
"""

from collections import Counter

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        left, right = zip(*(map(int, line.split()) for line in data_file))
        return (sorted(left), sorted(right))


def day01_part1(data):
    return sum(abs(a - b) for a, b in zip(*data))


def day01_part2(data):
    left_list, right_list = data
    count = Counter(right_list)
    return sum(a * count[a] for a in left_list)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day01_test.txt")


def test_day01_part1(test_data):
    assert day01_part1(test_data) == 11


def test_day01_part2(test_data):
    assert day01_part2(test_data) == 31


if __name__ == "__main__":
    input_data = parse_input("data/day01.txt")

    print("Day 01 Part 1:")
    print(day01_part1(input_data))

    print("Day 01 Part 2:")
    print(day01_part2(input_data))
