"""
Advent of Code 2024
Day 21: Keypad Conundrum
"""

from itertools import product

import pytest

Coordinates = tuple[int, int]

NUM_PAD_COORD = {
    c: (x, y)
    for y, row in enumerate(["789", "456", "123", " 0A"])
    for x, c in enumerate(row)
}
DIR_PAD_COORD = {
    c: (x, y) for y, row in enumerate([" ^A", "<v>"]) for x, c in enumerate(row)
}


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().splitlines()


def move_sequence(p1: Coordinates, p2: Coordinates) -> tuple[str, str]:
    (x1, y1), (x2, y2) = p1, p2
    horizontal_moves = (">" if x2 > x1 else "<") * abs(x2 - x1)
    vertical_moves = ("^" if y2 < y1 else "v") * abs(y2 - y1)
    return horizontal_moves, vertical_moves


def press_cost(path: str, prev_layer: dict[tuple[str, str], int]) -> int:
    try:
        return sum(prev_layer[(a, b)] for a, b in zip("A" + path, path))
    except KeyError as e:
        raise ValueError(
            f"Invalid path segment {e.args[0]} not found in previous layer."
        ) from e


def compute_layer(
    prev_layer: dict[tuple[str, str], int], keys: dict[str, Coordinates]
) -> dict[tuple[str, str], int]:
    skip = keys.get(" ", (-1, -1))
    result = {}
    for (ki, pi), (kf, pf) in product(keys.items(), repeat=2):
        h, v = move_sequence(pi, pf)
        cost1 = (
            press_cost(h + v + "A", prev_layer)
            if (pf[0], pi[1]) != skip
            else float("inf")
        )
        cost2 = (
            press_cost(v + h + "A", prev_layer)
            if (pi[0], pf[1]) != skip
            else float("inf")
        )
        result[(ki, kf)] = min(cost1, cost2)
    return result


def build_leg_lengths(n: int) -> dict[tuple[str, str], int]:
    layer = {(ki, kf): 1 for ki, kf in product(DIR_PAD_COORD, repeat=2)}
    for _ in range(n - 1):
        layer = compute_layer(layer, DIR_PAD_COORD)
    return compute_layer(layer, NUM_PAD_COORD)


def calc_fewest(code: str, num_layers: int) -> int:
    legs = build_leg_lengths(num_layers)
    return sum(legs[ki, kf] for ki, kf in zip("A" + code, code))


def day21_part1(data: list[str]) -> int:
    return sum(calc_fewest(code, 3) * int(code[:-1]) for code in data)


def day21_part2(data: list[str]) -> int:
    return sum(calc_fewest(code, 26) * int(code[:-1]) for code in data)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day21_test.txt")


def test_day21_part1(test_data):
    assert day21_part1(test_data) == 126384


def test_day21_part2(test_data):
    assert day21_part2(test_data) == 154115708116294


if __name__ == "__main__":
    input_data = parse_input("data/day21.txt")

    print("Day 21 Part 1:")
    print(day21_part1(input_data))

    print("Day 21 Part 2:")
    print(day21_part2(input_data))
