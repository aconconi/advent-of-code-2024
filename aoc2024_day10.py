"""
Advent of Code 2024
Day 10: Hoof It
"""

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return Grid(data_file.read().splitlines())


class Grid:
    def __init__(self, grid_strings):
        self.grid = [list(row) for row in grid_strings]
        self.heigth = len(self.grid)
        self.width = len(self.grid[0]) if self.heigth > 0 else 0
        self.trailheads = set()
        self.destinations = set()

        for y, row in enumerate(grid_strings):
            for x, cell in enumerate(row):
                match cell:
                    case "0":
                        self.trailheads.add((x, y))
                    case "9":
                        self.destinations.add((x, y))

    def is_inside(self, pos):
        x, y = pos
        return (0 <= x < self.width) and (0 <= y < self.heigth)

    def get_height(self, pos):
        x, y = pos
        return int(self.grid[y][x])

    def gen_neighbours(self, pos):
        x, y = pos
        height = self.get_height(pos)
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            new_pos = x + dx, y + dy
            if self.is_inside(new_pos) and self.get_height(new_pos) - height == 1:
                yield new_pos


def paths(grid, start):
    stack = [[start]]
    paths = set()
    while stack:
        path = stack.pop()
        pos = path[-1]
        if pos in grid.destinations:
            paths.add(tuple(path))
        else:
            stack.extend(
                path + [new_pos]
                for new_pos in grid.gen_neighbours(pos)
                if new_pos not in path
            )
    return paths


def day10_part1(grid):
    def score(pos):
        return len(set(path[-1] for path in paths(grid, pos)))

    return sum(score(trailhead) for trailhead in grid.trailheads)


def day10_part2(grid):
    def rating(pos):
        return len(paths(grid, pos))

    return sum(rating(trailhead) for trailhead in grid.trailheads)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day10_test.txt")


def test_day10_part1(test_data):
    assert day10_part1(test_data) == 36


def test_day10_part2(test_data):
    assert day10_part2(test_data) == 81


if __name__ == "__main__":
    input_data = parse_input("data/day10.txt")

    print("Day 10 Part 1:")
    print(day10_part1(input_data))  # Correct answer is 587

    print("Day 10 Part 2:")
    print(day10_part2(input_data))  # Correct answer is 1340
