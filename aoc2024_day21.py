"""
Advent of Code 2024
Day 21: Keypad Conundrum
"""

from collections import deque
from itertools import combinations, product
import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().splitlines()


NUM_PAD_COORD = {c: (x, y) for y, row in enumerate(["789", "456", "123", " 0A"]) for x, c in enumerate(row)}
DIR_PAD_COORD = {c: (x, y) for y, row in enumerate([" ^A", "<v>"]) for x, c in enumerate(row)}


def initial_layer() -> dict[tuple[str, str], int]:
    return {(ki, kf): 1 for ki, kf in product(DIR_PAD_COORD, repeat=2)}

def move_sequence(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[str, str]:
    (x1, y1), (x2, y2) = p1, p2
    h = ('>' if x2 > x1 else '<') * abs(x2 - x1)
    v = ('^' if y2 < y1 else 'v') * abs(y2 - y1)
    return h, v

def press_cost(path: str, prev_layer: dict[tuple[str, str], int]) -> int:
    return sum(prev_layer.get((a, b), float('inf')) for a, b in zip('A' + path, path))

def compute_layer(prev_layer: dict[tuple[str, str], int], keys: dict[str, tuple[int, int]]) -> dict[tuple[str, str], int]:
    skip = keys.get(' ', (-1, -1))
    result = {}
    for (ki, pi), (kf, pf) in product(keys.items(), repeat=2):
        h, v = move_sequence(pi, pf)
        cost1 = press_cost(h + v + 'A', prev_layer) if (pf[0], pi[1]) != skip else float('inf')
        cost2 = press_cost(v + h + 'A', prev_layer) if (pi[0], pf[1]) != skip else float('inf')
        result[(ki, kf)] = min(cost1, cost2)
    return result

def build_leg_lengths(n: int) -> dict[tuple[str, str], int]:
    layers = [initial_layer()]
    for i in range(1, n + 1):
        keys = NUM_PAD_COORD if i == n else DIR_PAD_COORD
        layers.append(compute_layer(layers[-1], keys))
    return layers[-1]

def calc_fewest(code: str, n_layers: int) -> int:
    legs = build_leg_lengths(n_layers)
    return sum(legs[ki, kf] for ki, kf in zip('A' + code, code))

def day21_part1(data: list[str]) -> int:
    return sum(calc_fewest(code, 3)  * int(code[:-1]) for code in data)

def day21_part2(data: list[str]) -> int:
    return sum(calc_fewest(code, 26) * int(code[:-1]) for code in data)



@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day21_test.txt")


def test_day20_part1(test_data):
    pass

def test_day20_part2(test_data):
    pass

if __name__ == "__main__":
    input_data = parse_input("data/day21.txt")

    print("Day 21 Part 1:")
    print(day21_part1(input_data))  # Correct answer is

    print("Day 21 Part 2:")
    print(day21_part2(input_data))  # Correct answer is
