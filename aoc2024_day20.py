"""
Advent of Code 2024
Day 20: Race Condition
"""

from collections import deque
from itertools import combinations

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        rows = data_file.read().splitlines()
        walkable = {
            (x, y)
            for y, row in enumerate(rows)
            for x, cell in enumerate(row)
            if cell in ".SE"
        }
        start = next(
            (x, y)
            for y, row in enumerate(rows)
            for x, cell in enumerate(row)
            if cell == "S"
        )
        return walkable, start


def gen_neighbors(walkable, pos):
    x, y = pos
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        neighbor = (x + dx, y + dy)
        if neighbor in walkable:
            yield neighbor


def distances(
    walkable: set[tuple[int, int]], start: tuple[int, int]
) -> dict[tuple[int, int], int]:
    dist = {start: 0}
    queue = deque([start])
    while queue:
        pos = queue.popleft()
        for neighbor in gen_neighbors(walkable, pos):
            if neighbor not in dist:
                dist[neighbor] = dist[pos] + 1
                queue.append(neighbor)
    return dist


def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def solve(walkable, start, min_saving, max_distance):
    count = 0
    dist = distances(walkable, start)
    for (pos_a, dist_a), (pos_b, dist_b) in combinations(dist.items(), 2):
        d = manhattan(pos_a, pos_b)
        if d <= max_distance and dist_b - dist_a - d >= min_saving:
            count += 1
    return count


def day20_part1(data):
    return solve(*data, min_saving=100, max_distance=2)


def day20_part2(data):
    return solve(*data, min_saving=100, max_distance=20)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day20_test.txt")


def test_day20_part1(test_data):
    assert solve(*test_data, min_saving=1, max_distance=2) == 44


def test_day20_part2(test_data):
    assert solve(*test_data, min_saving=50, max_distance=20) == 285


if __name__ == "__main__":
    input_data = parse_input("data/day20.txt")

    print("Day 20 Part 1:")
    print(day20_part1(input_data))  # Correct answer is 1307

    print("Day 20 Part 2:")
    print(day20_part2(input_data))  # Correct answer is 986545
