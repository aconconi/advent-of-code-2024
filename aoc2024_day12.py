"""
Advent of Code 2024
Day 12: Garden Groups
"""

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return Grid(data_file.read().splitlines())


class Grid:
    def __init__(self, grid_strings):
        self.grid = [list(row) for row in grid_strings]
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.height > 0 else 0

    def is_inside(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def get(self, pos):
        x, y = pos
        return self.grid[y][x] if self.is_inside(pos) else None

    def gen_neighbors(self, pos, allow_external=False):
        x, y = pos
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            new_pos = x + dx, y + dy
            if self.is_inside(new_pos) or allow_external:
                yield new_pos

    def gen_positions(self):
        # Generate all grid positions (x, y)
        yield from ((x, y) for x in range(self.width) for y in range(self.height))

    def find_region(self, start_pos):
        target_value = self.get(start_pos)
        visited = set()

        def flood(pos):
            # If position is valid and matches the target value, process it
            if pos not in visited and self.get(pos) == target_value:
                visited.add(pos)
                yield pos  # Yield the current position
                # Recursively visit all neighboring positions
                for neighbor in self.gen_neighbors(pos):
                    yield from flood(neighbor)

        # Start the flood fill from the starting position
        yield from flood(start_pos)

    def find_regions(self):
        plots = set(self.gen_positions())
        while plots:
            plot = plots.pop()
            region = set(self.find_region(plot))
            plots -= region
            yield region


def score_region(grid: Grid, start_pos: tuple[int, int]) -> int:
    target = grid.get(start_pos)
    if target is None:
        return 0

    seen = set()
    area = 0
    perimeter = 0
    stack = [start_pos]

    while stack:
        pos = stack.pop()
        if pos in seen or grid.get(pos) != target:
            continue
        seen.add(pos)
        area += 1
        x, y = pos

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if grid.get(neighbor) != target:
                perimeter += 1
                # Corner correction logic to reduce over-counting
                if (
                    (dx, dy) == (0, 1)
                    and grid.get((x + 1, y)) == target
                    and grid.get((x + 1, y + 1)) != target
                ):
                    perimeter -= 1
                elif (
                    (dx, dy) == (0, -1)
                    and grid.get((x + 1, y)) == target
                    and grid.get((x + 1, y - 1)) != target
                ):
                    perimeter -= 1
                elif (
                    (dx, dy) == (1, 0)
                    and grid.get((x, y + 1)) == target
                    and grid.get((x + 1, y + 1)) != target
                ):
                    perimeter -= 1
                elif (
                    (dx, dy) == (-1, 0)
                    and grid.get((x, y + 1)) == target
                    and grid.get((x - 1, y + 1)) != target
                ):
                    perimeter -= 1
            else:
                if neighbor not in seen:
                    stack.append(neighbor)

    return area * perimeter


def get_perimeter(grid, region):
    return sum(
        neigh not in region
        for pos in region
        for neigh in grid.gen_neighbors(pos, allow_external=True)
    )


def day12_part1(grid):
    return sum(
        len(region) * get_perimeter(grid, region) for region in grid.find_regions()
    )


def day12_part2(grid):
    return sum(score_region(grid, list(region)[0]) for region in grid.find_regions())


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day12_test.txt")


def test_day12_part1(test_data):
    assert day12_part1(test_data) == 1930


def test_day12_part2(test_data):
    assert day12_part2(test_data) == 1206


if __name__ == "__main__":
    input_data = parse_input("data/day12.txt")

    print("Day 12 Part 1:")
    print(day12_part1(input_data))  # Correct answer is 1363484

    print("Day 12 Part 2:")
    print(day12_part2(input_data))  # Correct answer is 838988
