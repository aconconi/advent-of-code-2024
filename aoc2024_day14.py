"""
Advent of Code 2024
Day 14: Restroom Redoubt
"""

import re
from itertools import count

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return [
            tuple(map(int, re.findall(r"-?\d+", line)))
            for line in data_file.read().splitlines()
        ]


def step(robots, width, height):
    return [((x + vx) % width, (y + vy) % height, vx, vy) for x, y, vx, vy in robots]


def count_quadrants(robots, width, height):
    mid_x, mid_y = width // 2, height // 2
    quadrants = [0] * 4
    for x, y, _, _ in robots:
        if x == mid_x or y == mid_y:
            continue
        quadrants[(x < mid_x) + 2 * (y < mid_y)] += 1
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def day14_part1(robots, width, height):
    for _ in range(100):
        robots = step(robots, width, height)
    return count_quadrants(robots, width, height)


def day14_part2(robots, width, height):
    for seconds in count(1):
        robots = step(robots, width, height)
        if len(robots) == len(set((x, y) for x, y, _, _ in robots)):
            return seconds


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day14_test.txt")


def test_day14_part1(test_data):
    assert day14_part1(test_data, width=11, height=7) == 12


if __name__ == "__main__":
    input_data = parse_input("data/day14.txt")

    print("Day 14 Part 1:")
    print(day14_part1(input_data, width=101, height=103))  # Correct answer is 219512160

    print("Day 14 Part 2:")
    print(day14_part2(input_data, width=101, height=103))  # Correct answer is 6398
