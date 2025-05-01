"""
Advent of Code 2024
Day 22: Monkey Market
"""

from collections import defaultdict

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return list(map(int, data_file.read().splitlines()))


def evolve(number: int) -> int:
    number = (number ^ (number * 64)) % 16777216
    number = (number ^ (number // 32)) % 16777216
    number = (number ^ (number * 2048)) % 16777216
    return number


def day22_part1(data: list[int]) -> int:

    def repeat_func(func, value, steps):
        for _ in range(steps):
            value = func(value)
        return value

    return sum(repeat_func(evolve, number, 2000) for number in data)


def day22_part2(data: list[int]) -> int:
    sequences = defaultdict(list)

    for number in data:
        monkey = [number % 10]  # Initial price
        monkey_sequences = set()

        for i in range(2000):
            number = evolve(number)
            price = number % 10
            monkey.append(price)

            if i >= 3:
                # Create the sequence and check if it's a new one
                sequence = tuple(monkey[j] - monkey[i - 3] for j in range(i - 2, i + 2))
                if sequence not in monkey_sequences:
                    monkey_sequences.add(sequence)
                    sequences[sequence].append(price)

    return max(sum(sequence) for sequence in sequences.values())

@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day22_test.txt")


def test_day22_part1(test_data):
    assert day22_part1(test_data) == 37327623


def test_day22_part2(test_data):
    assert day22_part2(test_data) == 24


if __name__ == "__main__":
    input_data = parse_input("data/day22.txt")

    print("Day 22 Part 1:")
    print(day22_part1(input_data))  # Correct answer is 18317943467

    print("Day 22 Part 2:")
    print(day22_part2(input_data))  # Correct answer is 2018
