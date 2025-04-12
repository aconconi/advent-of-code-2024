"""
Advent of Code 2024
Day 15: Warehouse Woes
"""

import pytest

DIRMOVE = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}


class Grid:
    def __init__(self, grid_data):
        grid_lines = grid_data.splitlines()
        self.grid = [list(row) for row in grid_lines]
        self.submarine = next(
            (x, y)
            for y, row in enumerate(self.grid)
            for x, cell in enumerate(row)
            if cell == "@"
        )

    def get(self, pos):
        x, y = pos
        return self.grid[y][x]

    def set(self, pos, value):
        x, y = pos
        self.grid[y][x] = value

    def score(self):
        return sum(
            x + y * 100
            for y, row in enumerate(self.grid)
            for x, cell in enumerate(row)
            if cell in "O["
        )

    def __str__(self):
        return "\n".join("".join(row) for row in self.grid)


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        grid_data, dir_data = data_file.read().split("\n\n")
    return grid_data, "".join(line.strip() for line in dir_data)


def step(pos, dir):
    x, y = pos
    dx, dy = DIRMOVE[dir]
    return x + dx, y + dy


def can_move(grid, pos, dir):
    next_pos = step(pos, dir)
    next_val = grid.get(next_pos)
    ans = False
    match next_val:
        case ".":
            ans = True
        case "O":
            ans = can_move(grid, next_pos, dir)
        case "[" | "]" if dir in "><":
            ans = can_move(grid, next_pos, dir)
        case "[" | "]" if dir in "^v":
            other_pos = step(next_pos, "<") if next_val == "]" else step(next_pos, ">")
            ans = can_move(grid, next_pos, dir) and can_move(grid, other_pos, dir)
    return ans


def move(grid, pos, dir):
    current_val = grid.get(pos)
    next_pos = step(pos, dir)
    next_val = grid.get(next_pos)
    match next_val:
        case ".":
            grid.set(pos, ".")
            grid.set(next_pos, current_val)
            if current_val == "@":
                grid.submarine = next_pos
        case "O":
            move(grid, next_pos, dir)
            move(grid, pos, dir)
        case "[" | "]":
            move(grid, next_pos, dir)
            if dir in "^v":
                other_pos = (
                    step(next_pos, "<") if next_val == "]" else step(next_pos, ">")
                )
                move(grid, other_pos, dir)
            move(grid, pos, dir)


def solve(grid_data, directions):
    grid = Grid(grid_data)
    for dir in directions:
        if can_move(grid, grid.submarine, dir):
            move(grid, grid.submarine, dir)
    return grid.score()


def day15_part1(data):
    return solve(*data)


def day15_part2(data):
    grid_data, directions = data
    transformed_grid_data = "\n".join(
        s.replace(".", "..").replace("#", "##").replace("@", "@.").replace("O", "[]")
        for s in grid_data.splitlines()
    )
    return solve(transformed_grid_data, directions)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day15_test.txt")


def test_day15_part1(test_data):
    assert day15_part1(test_data) == 10092


def test_day15_part2(test_data):
    assert day15_part2(test_data) == 9021


if __name__ == "__main__":
    input_data = parse_input("data/day15.txt")

    print("Day 15 Part 1:")
    print(day15_part1(input_data))  # Correct answer is 1438161

    print("Day 15 Part 2:")
    print(day15_part2(input_data))  # Correct answer is 1437981
