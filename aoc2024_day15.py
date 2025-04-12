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

    def can_move(self, pos, dir):
        next_pos = step(pos, dir)
        next_value = self.get(next_pos)
        if next_value == ".":
            return True
        if next_value == "O":
            return self.can_move(next_pos, dir)
        return False  # Wall

    def move(self, pos, dir):
        current_value = self.get(pos)
        next_pos = step(pos, dir)
        next_value = self.get(next_pos)

        if next_value == ".":
            self.set(pos, ".")
            self.set(next_pos, current_value)
            if current_value == "@":
                self.submarine = next_pos
        elif next_value == "O":
            self.move(next_pos, dir)
            self.move(pos, dir)

    def can_move2(self, pos, dir):
        next_pos = step(pos, dir)
        next_value = self.get(next_pos)
        # Space
        if next_value == ".":
            ans = True
        elif next_value == "#":
            ans = False
        elif dir in "><":
            ans = self.can_move2(next_pos, dir)
        else:
            other_pos = (
                step(next_pos, "<") if next_value == "]" else step(next_pos, ">")
            )
            ans = self.can_move2(next_pos, dir) and self.can_move2(other_pos, dir)
        return ans

    def move2(self, pos, dir):
        current_value = self.get(pos)
        next_pos = step(pos, dir)
        next_value = self.get(next_pos)
        if next_value == ".":
            self.set(pos, ".")
            self.set(next_pos, current_value)
            if current_value == "@":
                self.submarine = next_pos
        elif next_value in "[]":
            self.move2(next_pos, dir)
            if dir in "^v":
                other_pos = (
                    step(next_pos, "<") if next_value == "]" else step(next_pos, ">")
                )
                self.move2(other_pos, dir)
            self.move2(pos, dir)

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


def day15_part1(data):
    grid_data, directions = data
    grid = Grid(grid_data)
    for dir in directions:
        if grid.can_move(grid.submarine, dir):
            grid.move(grid.submarine, dir)
    return grid.score()


def day15_part2(data):
    grid_data, directions = data
    grid = Grid(grid_data, double=True)
    for dir in directions:
        if grid.can_move2(grid.submarine, dir):
            grid.move2(grid.submarine, dir)
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
    input_data = parse_input("data/day15.txt")

    print("Day 15 Part 1:")
    print(day15_part1(input_data))  # Correct answer is 1438161

    print("Day 15 Part 2:")
    print(day15_part2(input_data))  # Correct answer is 1437981
