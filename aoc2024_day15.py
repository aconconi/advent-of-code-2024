"""
Advent of Code 2024
Day 15:
"""

# pylint: skip-file

DIRMOVE = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}


class Grid:
    def __init__(self, grid_data, double=False):
        if not double:
            grid_lines = grid_data.splitlines()
        else:
            grid_lines = [
                s.replace(".", "..")
                .replace("#", "##")
                .replace("@", "@.")
                .replace("O", "[]")
                for s in grid_data.splitlines()
            ]
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

    def commit(self, pos, next_pos):
        value = self.get(pos)
        self.set(pos, ".")
        self.set(next_pos, value)
        if value == "@":
            self.submarine = next_pos

    def move(self, pos, dir):
        next_pos = step(pos, dir)
        if self.get(next_pos) == "." or (
            self.get(next_pos) == "O" and self.move(next_pos, dir)
        ):
            self.commit(pos, next_pos)
            return True
        return False

    def move2(self, pos, dir):
        next_pos = step(pos, dir)
        if self.get(next_pos) == ".":
            self.commit(pos, next_pos)
            return True
        if self.get(next_pos) == "#":
            return False
        # it's a box
        if dir in "><":
            if self.move2(next_pos, dir):
                self.commit(pos, next_pos)
                return True
        other_pos = (
            step(next_pos, "<") if self.get(next_pos) == "]" else step(next_pos, ">")
        )
        if self.move2(next_pos, dir) and self.move2(other_pos, dir):  # WRONG
            self.commit(pos, next_pos)
            return True

    # box with vertical movement, the hard case

    def score(self):
        return sum(
            x + y * 100
            for y, row in enumerate(self.grid)
            for x, cell in enumerate(row)
            if cell == "O"
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


def day15_part1(data):
    grid_data, directions = data
    grid = Grid(grid_data)
    print(grid)
    pos = grid.submarine
    print("submarine at", pos)
    for dir in directions:
        print(f"\nMove {dir}:")
        grid.move(grid.submarine, dir)
        print(grid)
    return grid.score()


def day15_part2(data):
    grid_data, directions = data
    grid = Grid(grid_data, double=True)
    pos = grid.submarine
    print("submarine at", pos)
    for dir in directions:
        print(f"\nMove {dir}:")
        grid.move2(grid.submarine, dir)
        print(grid)
    return grid.score()


"""
@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day15_test.txt")


def test_day15_part1(test_data):
    assert day15_part1(test_data) == 2028

def test_day15_part2(test_data):
    assert day15_part2(test_data)
"""

if __name__ == "__main__":
    input_data = parse_input("data/day15_test3.txt")

    # print("Day 15 Part 1:")
    # print(day15_part1(input_data))  # Correct answer is 1438161

    print("Day 15 Part 2:")
    print(day15_part2(input_data))  # Correct answer is
