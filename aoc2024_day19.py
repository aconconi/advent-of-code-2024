"""
Advent of Code 2024
Day 19:
"""

# pylint: skip-file
import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().splitlines()


def day19_part1(data):
    pass


def day19_part2(data):
    pass


"""
@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day19_test.txt")


def test_day19_part1(test_data):
    assert day19_part1(test_data)

def test_day19_part2(test_data):
    assert day19_part2(test_data)
"""

if __name__ == "__main__":
    input_data = parse_input("data/day19_test.txt")

    print("Day 19 Part 1:")
    print(day19_part1(input_data))  # Correct answer is

    print("Day 19 Part 2:")
    print(day19_part2(input_data))  # Correct answer is
