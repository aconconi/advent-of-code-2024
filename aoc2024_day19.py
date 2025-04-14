"""
Advent of Code 2024
Day 19:
"""

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        lines = data_file.read().splitlines()
    return (lines[0].split(", "), lines[2:])


def solve(design, towels):
    stack = [design]
    while stack:
        current = stack.pop()
        for towel in towels:
            if towel == current:
                return True
            if current.startswith(towel):
                stack.append(current[len(towel) :])
    return False


def count_solutions(design: str, towels: set[str]) -> int:
    n = len(design)
    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        for towel in towels:
            if design.startswith(towel, i - len(towel)):
                dp[i] += dp[i - len(towel)]

    return dp[n]


def day19_part1(data):
    towels, designs = data
    return sum(solve(design, towels) for design in designs)


def day19_part2(data):
    towels, designs = data
    return sum(count_solutions(design, towels) for design in designs)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day19_test.txt")


def test_day19_part1(test_data):
    assert day19_part1(test_data) == 6


def test_day19_part2(test_data):
    assert day19_part2(test_data) == 16


if __name__ == "__main__":
    input_data = parse_input("data/day19.txt")

    print("Day 19 Part 1:")
    print(day19_part1(input_data))  # Correct answer is 263

    print("Day 19 Part 2:")
    print(day19_part2(input_data))  # Correct answer is 723524534506343
