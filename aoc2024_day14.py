"""
Advent of Code 2024
Day 14:
"""

# pylint: skip-file
import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().splitlines()


def day14_part1(data):
    pass


def day14_part2(data):
    pass


"""
@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day14_test.txt")


def test_day14_part1(test_data):
    assert day14_part1(test_data)

def test_day14_part2(test_data):
    assert day14_part2(test_data)
"""

if __name__ == "__main__":
    input_data = parse_input("data/day14_test.txt")

    print("Day 14 Part 1:")
    print(day14_part1(input_data))  # Correct answer is

    print("Day 14 Part 2:")
    print(day14_part2(input_data))  # Correct answer is
