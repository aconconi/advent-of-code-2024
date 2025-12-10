"""
Advent of Code 2024
Day 04: Ceres Search
"""

import re

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().splitlines()


def matrix_elements(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    # Yield rows
    yield from matrix

    # Yield columns
    yield from (
        "".join(matrix[row][col] for row in range(num_rows)) for col in range(num_cols)
    )

    # Yield left diagonals (top-left to bottom-right)
    yield from (
        "".join(
            matrix[row][diag - row]
            for row in range(num_rows)
            if 0 <= diag - row < num_cols
        )
        for diag in range(num_rows + num_cols - 1)
    )

    # Yield right diagonals (top-right to bottom-left)
    yield from (
        "".join(
            matrix[row][diag - (num_cols - 1 - row)]
            for row in range(num_rows)
            if 0 <= diag - (num_cols - 1 - row) < num_cols
        )
        for diag in range(num_rows + num_cols - 1)
    )


def day04_part1(data):
    return sum(len(re.findall("(?=XMAS|SAMX)", s)) for s in matrix_elements(data))


def day04_part2(data):
    def is_x_mas(i, j):
        if data[i][j] != "A":
            return False
        left_diag = {data[i - 1][j - 1], data[i + 1][j + 1]}
        right_diag = {data[i - 1][j + 1], data[i + 1][j - 1]}
        return left_diag == right_diag == {"M", "S"}

    return sum(
        is_x_mas(i, j)
        for i in range(1, len(data) - 1)
        for j in range(1, len(data[0]) - 1)
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day04_test.txt")


def test_day04_part1(test_data):
    assert day04_part1(test_data) == 18


def test_day04_part2(test_data):
    assert day04_part2(test_data) == 9


if __name__ == "__main__":
    input_data = parse_input("data/day04.txt")

    print("Day 04 Part 1:")
    print(day04_part1(input_data))

    print("Day 04 Part 2:")
    print(day04_part2(input_data))
