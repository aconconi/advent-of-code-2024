"""
Advent of Code 2024
Day 11: Plutonian Pebbles
"""

from functools import cache

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return list(map(int, data_file.read().split()))


@cache
def blink(stone, num_steps):
    if num_steps == 0:
        return 1

    str_stone = str(stone)
    len_stone = len(str_stone)
    num_steps -= 1
    if stone == 0:
        return blink(1, num_steps)
    if len_stone % 2 == 0:
        left_stone = int(str_stone[: len_stone // 2])
        right_stone = int(str_stone[len_stone // 2 :])
        return blink(left_stone, num_steps) + blink(right_stone, num_steps)
    return blink(stone * 2024, num_steps)


def day11_part1(data):
    return sum(blink(stone, 25) for stone in data)


def day11_part2(data):
    return sum(blink(stone, 75) for stone in data)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day11_test.txt")


def test_day11_part1(test_data):
    assert day11_part1(test_data) == 55312


def test_day11_part2(test_data):
    assert day11_part2(test_data) == 65601038650482


if __name__ == "__main__":
    input_data = parse_input("data/day11.txt")

    print("Day 11 Part 1:")
    print(day11_part1(input_data))

    print("Day 11 Part 2:")
    print(day11_part2(input_data))
