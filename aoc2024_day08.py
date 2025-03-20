"""
Advent of Code 2024
Day 08:
"""

from collections import defaultdict
from itertools import combinations

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


def get_antinodes(a, b, size):
    def offset(a, b):
        return 2 * b[0] - a[0], 2 * b[1] - a[1]

    return {
        pos
        for pos in [offset(a, b), offset(b, a)]
        if 0 <= pos[0] < size and 0 <= pos[1] < size
    }


def get_antinodes2(a, b, size):
    x1, y1 = a
    x2, y2 = b
    dx = x2 - x1
    dy = y2 - y1

    def generate_points(direction):
        k = 0 if direction == 1 else -1
        while True:
            x, y = x1 + k * dx, y1 + k * dy
            if 0 <= x < size and 0 <= y < size:
                yield (x, y)
            else:
                break
            k += direction

    return set(generate_points(1)) | set(generate_points(-1))


def day08_part1(data):
    map_freq_ant, size = data
    antinodes = {
        antinode
        for frequency, antennas in map_freq_ant.items()
        for pair in combinations(antennas, 2)
        for antinode in get_antinodes(*pair, size)
    }
    return len(antinodes)


def day08_part2(data):
    map_freq_ant, size = data
    antinodes = {
        antinode
        for frequency, antennas in map_freq_ant.items()
        for pair in combinations(antennas, 2)
        for antinode in get_antinodes2(*pair, size)
    }
    return len(antinodes)


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
