"""
Advent of Code 2024
Day 25: Code Chronicle
"""

from itertools import product

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        schematics = map(str.splitlines, data_file.read().split("\n\n"))
    lock_schematics = []
    key_schematics = []
    for s in schematics:
        entry = tuple(sum(s[i][j] == "#" for i in range(1, 6)) for j in range(5))
        if s[0].startswith("#"):
            lock_schematics.append(entry)
        else:
            key_schematics.append(entry)
    return lock_schematics, key_schematics


def day25_part1(data):
    lock_schematics, key_schematics = data

    def is_fit(lock_schematic, key_schematic):
        return all(pin + edge <= 5 for pin, edge in zip(lock_schematic, key_schematic))

    return sum(
        is_fit(lock_schematic, key_schematic)
        for lock_schematic, key_schematic in product(lock_schematics, key_schematics)
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day25_test.txt")


def test_day25_part1(test_data):
    assert day25_part1(test_data) == 3


if __name__ == "__main__":
    input_data = parse_input("data/day25.txt")

    print("Day 25 Part 1:")
    print(day25_part1(input_data))

    # There is no part 2 to be solved on this day :-)
