"""
Advent of Code 2024
Day 06: Guard Gallivant
"""

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        grid_strings = data_file.read().splitlines()
        return Grid(grid_strings)


class Grid:
    def __init__(self, grid_strings):
        self.grid = [list(row) for row in grid_strings]
        self.heigth = len(self.grid)
        self.width = len(self.grid[0]) if self.heigth > 0 else 0
        self.start = next(
            (x, y)
            for y, row in enumerate(grid_strings)
            for x, cell in enumerate(row)
            if cell == "^"
        )

    def is_inside(self, pos):
        x, y = pos
        return (0 <= x < self.width) and (0 <= y < self.heigth)

    def get(self, pos):
        x, y = pos
        return self.grid[y][x] if self.is_inside(pos) else None

    def step(self, pos, dir):
        x, y = pos
        dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][dir]
        return (x + dx, y + dy)


def day06_part1(grid):
    pos = grid.start
    dir = 0
    seen = set()
    while True:
        seen.add(pos)
        new_pos = grid.step(pos, dir)
        match grid.get(new_pos):
            case None:
                # went off the grid, we are done
                return len(seen)
            case "#":
                # hit a wall, turn right
                dir = (dir + 1) % 4
            case _:
                # move forward
                pos = new_pos


def day06_part2x(grid):
    def is_loop(grid, obstruction):
        pos = grid.start
        dir = 0
        seen = set()
        while True:
            if grid.get(pos) is None:
                # went off the grid, no looop
                return False
            if (pos, dir) in seen:
                # loop found
                return True
            seen.add((pos, dir))
            while (
                grid.get(new_pos := grid.step(pos, dir)) == "#"
                or new_pos == obstruction
            ):
                dir = (dir + 1) % 4
            pos = new_pos


def day06_part2(grid):
    def is_loop(grid, obstruction):
        pos = grid.start
        dir = 0
        seen = set()
        while True:
            if (pos, dir) in seen:
                # loop found
                return True
            seen.add((pos, dir))
            new_pos = grid.step(pos, dir)
            cell = "#" if new_pos == obstruction else grid.get(new_pos)
            match cell:
                case None:
                    # went off the grid, no loop detected
                    return False
                case "#":
                    # hit a wall (or obstruction), turn right
                    dir = (dir + 1) % 4
                case _:
                    # move forward
                    pos = new_pos

    return sum(
        is_loop(grid, (x, y))
        for x in range(grid.width)
        for y in range(grid.heigth)
        if grid.get((x, y)) == "."
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day06_test.txt")


def test_day06_part1(test_data):
    assert day06_part1(test_data) == 41


def test_day06_part2(test_data):
    assert day06_part2(test_data) == 6


if __name__ == "__main__":
    input_data = parse_input("data/day06.txt")

    print("Day 06 Part 1:")
    print(day06_part1(input_data))  # Correct answer is 5080

    print("Day 06 Part 2:")
    print(day06_part2(input_data))  # Correct answer is 1919
