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


def gen_monkey_sequences(number: int):
    prices = [number % 10]
    seen = set()

    for _ in range(2000):
        number = evolve(number)
        price = number % 10
        prices.append(price)
        if len(prices) < 5:
            continue
        sequence = tuple(x - prices[-5] for x in prices[-4:])
        if sequence not in seen:
            seen.add(sequence)
            yield sequence, price


def day22_part2(data: list[int]) -> int:
    seq_price_map = defaultdict(int)
    for number in data:
        for sequence, price in gen_monkey_sequences(number):
            seq_price_map[sequence] += price
    return max(seq_price_map.values())


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
