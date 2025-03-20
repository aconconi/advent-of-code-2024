"""
Advent of Code 2024
Day 08:
"""

from collections import defaultdict
from itertools import chain, combinations, count

import pytest


def parse_input(file_name):
    map_freq_ant = defaultdict(list)
    with open(file_name, "r", encoding="ascii") as data_file:
        lines = data_file.read().splitlines()
        size = len(lines)  # assuming the grid is a square
        for y, line in enumerate(lines):
            for x, frequency in enumerate(line):
                if frequency != ".":
                    map_freq_ant[frequency].append((x, y))
        return map_freq_ant, size


def generate_points_part1(start, end, size):
    dx, dy = end[0] - start[0], end[1] - start[1]
    x, y = end[0] + dx, end[1] + dy
    if 0 <= x < size and 0 <= y < size:
        yield (x, y)


def generate_points_part2(start, end, size):
    dx, dy = end[0] - start[0], end[1] - start[1]
    for k in count(1):
        x, y = start[0] + k * dx, start[1] + k * dy
        if 0 <= x < size and 0 <= y < size:
            yield (x, y)
        else:
            break


def solve(data, points_gen_func):
    map_freq_ant, size = data
    antinodes = {
        antinode
        for frequency, antennas in map_freq_ant.items()
        for pair in combinations(antennas, 2)
        for antinode in chain(
            points_gen_func(*pair, size), points_gen_func(*pair[::-1], size)
        )
    }
    return len(antinodes)


def day08_part1(data):
    return solve(data, generate_points_part1)


def day08_part2(data):
    return solve(data, generate_points_part2)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day08_test.txt")


def test_day08_part1(test_data):
    assert day08_part1(test_data) == 14


def test_day08_part2(test_data):
    assert day08_part2(test_data) == 34


if __name__ == "__main__":
    input_data = parse_input("data/day08.txt")

    print("Day 08 Part 1:")
    print(day08_part1(input_data))  # Correct answer is 265

    print("Day 08 Part 2:")
    print(day08_part2(input_data))  # Correct answer is 962
