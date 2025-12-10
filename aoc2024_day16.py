"""
Advent of Code 2024
Day 16: Reindeer Maze
"""

from heapq import heappop, heappush

import pytest

DIRMOVE = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}


class Grid:
    def __init__(self, grid_rows):
        self.grid = [list(row) for row in grid_rows]
        for y, row in enumerate(grid_rows):
            for x, cell in enumerate(row):
                if cell == "S":
                    self.start_pos = (x, y)
                elif cell == "E":
                    self.end_pos = (x, y)

    def get(self, pos):
        x, y = pos
        return self.grid[y][x]

    def __str__(self):
        return "\n".join("".join(row) for row in self.grid)

    @staticmethod
    def step(pos: tuple[int, int], direction: str) -> tuple[int, int]:
        x, y = pos
        dx, dy = DIRMOVE[direction]
        return x + dx, y + dy


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return Grid(data_file.read().splitlines())


def find_best_path(grid):
    queue = [(0, grid.start_pos, ">")]  # (cost, pos, prev_dir)
    visited = set()
    while queue:
        cost, pos, prev_dir = heappop(queue)
        if pos == grid.end_pos:
            return cost
        if (pos, prev_dir) in visited:
            continue
        visited.add((pos, prev_dir))
        for direction in DIRMOVE:
            next_pos = Grid.step(pos, direction)
            if grid.get(next_pos) != "#":
                new_cost = cost + 1 + (0 if direction == prev_dir else 1000)
                heappush(queue, (new_cost, next_pos, direction))
    return 0


def find_all_best_paths(grid):
    queue = [(0, grid.start_pos, ">", [grid.start_pos])]  # (cost, pos, prev_dir, path)
    costs = {}  # (pos, prev_dir) -> cost
    min_cost = float("inf")
    best_paths = []

    while queue:
        cost, pos, prev_dir, path = heappop(queue)
        if cost > min_cost:
            continue
        if pos == grid.end_pos:
            if cost < min_cost:
                min_cost = cost
                best_paths = [path]
            elif cost == min_cost:
                best_paths.append(path)
            continue

        key = (pos, prev_dir)
        if key in costs and costs[key] < cost:
            continue
        costs[key] = cost

        for direction in DIRMOVE:
            next_pos = Grid.step(pos, direction)
            if grid.get(next_pos) != "#":
                new_cost = cost + 1 + (0 if direction == prev_dir else 1000)
                heappush(queue, (new_cost, next_pos, direction, path + [next_pos]))

    return best_paths


def day16_part1(grid):
    return find_best_path(grid)


def day16_part2(grid):
    return len(set.union(*map(set, find_all_best_paths(grid))))


# Fixture for loading grid data
@pytest.fixture
def grid_test_data(request):
    file_name = request.param  # Get the file name from parametrize
    return parse_input(file_name)


# Parametrizing part1 test with the fixture
@pytest.mark.parametrize(
    "grid_test_data, expected_part1",
    [
        ("data/day16_test.txt", 7036),
        ("data/day16_test2.txt", 11048),
    ],
    indirect=[
        "grid_test_data"
    ],  # Indicating that grid_data should be handled by the fixture
)
def test_day16_part1(grid_test_data, expected_part1):
    assert day16_part1(grid_test_data) == expected_part1


# Parametrizing part2 test with the fixture
@pytest.mark.parametrize(
    "grid_test_data, expected_part2",
    [
        ("data/day16_test.txt", 45),
        ("data/day16_test2.txt", 64),
    ],
    indirect=[
        "grid_test_data"
    ],  # Indicating that grid_data should be handled by the fixture
)
def test_day16_part2(grid_test_data, expected_part2):
    assert day16_part2(grid_test_data) == expected_part2


if __name__ == "__main__":
    input_data = parse_input("data/day16.txt")

    print("Day 16 Part 1:")
    print(day16_part1(input_data))

    print("Day 16 Part 2:")
    print(day16_part2(input_data))
