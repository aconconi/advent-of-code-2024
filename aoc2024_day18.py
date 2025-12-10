"""
Advent of Code 2024
Day 18: RAM Run
"""

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return [
            tuple(map(int, line.split(","))) for line in data_file.read().splitlines()
        ]


def shortest_path_len(locations, start, end):
    queue = [(start, 0)]
    visited = set()
    while queue:
        current, distance = queue.pop(0)
        if current == end:
            return distance
        if current in visited:
            continue
        visited.add(current)
        for neighbor in [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1),
        ]:
            if neighbor in locations:
                queue.append((neighbor, distance + 1))
    return float("inf")


def day18_part1(falling, size, steps):
    locs = set(
        (x, y)
        for x in range(size)
        for y in range(size)
        if (x, y) not in set(falling[:steps])
    )
    start_loc = (0, 0)
    end_loc = (size - 1, size - 1)
    return shortest_path_len(locs, start_loc, end_loc)


def day18_part2(falling, size):
    locs = set((x, y) for x in range(size) for y in range(size))
    start_loc = (0, 0)
    end_loc = (size - 1, size - 1)
    for coord in falling:
        locs -= {coord}
        if shortest_path_len(locs, start_loc, end_loc) == float("inf"):
            return coord
    return None


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day18_test.txt")


def test_day18_part1(test_data):
    assert day18_part1(test_data, 7, 12) == 22


def test_day18_part2(test_data):
    assert day18_part2(test_data, 7) == (6, 1)


if __name__ == "__main__":
    input_data = parse_input("data/day18.txt")

    print("Day 18 Part 1:")
    print(day18_part1(input_data, 71, 1024))

    print("Day 18 Part 2:")
    print(day18_part2(input_data, 71))
