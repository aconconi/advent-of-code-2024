"""
Advent of Code 2024
Day 09: Disk Fragmenter
"""

from dataclasses import dataclass

import pytest

FREE_SPACE = "."
SPACE_id_number = -1


@dataclass(order=True)
class Sequence:
    start: int
    size: int
    id_number: int

    def __str__(self) -> str:
        return self.size * (str(self.id_number) if self.id_number >= 0 else ".")

    def checksum(self) -> int:
        return sum(
            self.id_number * i for i in range(self.start, self.start + self.size)
        )

    def gen_blocks(self):
        for i in range(self.size):
            yield self.start + i, self.id_number

    @classmethod
    def from_sequence(cls, sequence):
        return cls(sequence.start, sequence.size, sequence.id_number)


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        disk = data_file.read().rstrip()
    start = 0
    files = []
    spaces = []
    id_number = 0
    is_file = True
    for digit in disk:
        size = int(digit)
        if is_file:
            files.append(Sequence(start, size, id_number))
            id_number += 1
        else:
            if size > 0:
                spaces.append(Sequence(start, size, SPACE_id_number))
        start += size
        is_file = not is_file
    return files, spaces


def day09_part1(data):
    file_seqs = [Sequence.from_sequence(file_seq) for file_seq in data[0]]
    space_seqs = [Sequence.from_sequence(file_seq) for file_seq in data[1]]
    processed: list[Sequence] = []

    space_iter = iter(space_seqs)
    current_space = next(space_iter, None)

    for current_file in reversed(file_seqs):
        while (
            current_file.size > 0
            and current_space
            and current_space.start <= current_file.start
        ):
            move_size = min(current_file.size, current_space.size)
            processed.append(
                Sequence(
                    size=move_size,
                    start=current_space.start,
                    id_number=current_file.id_number,
                )
            )

            current_file.size -= move_size
            current_space.start += move_size
            current_space.size -= move_size

            if current_space.size == 0:
                current_space = next(space_iter, None)

        if current_file.size > 0:
            processed.append(current_file)

    return sum(seq.checksum() for seq in processed)


def day09_part2(data):
    file_seqs = [Sequence.from_sequence(file_seq) for file_seq in data[0]]
    space_seqs = [Sequence.from_sequence(file_seq) for file_seq in data[1]]
    processed: list[Sequence] = []
    for current_file in reversed(file_seqs):
        current_space = next(
            (
                s
                for s in space_seqs
                if s.size >= current_file.size and s.start < current_file.start
            ),
            None,
        )
        if current_space is None:
            processed.append(current_file)
        else:
            processed.append(
                Sequence(
                    start=current_space.start,
                    size=current_file.size,
                    id_number=current_file.id_number,
                )
            )
            current_space.start += current_file.size
            current_space.size -= current_file.size

    return sum(seq.checksum() for seq in processed)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day09_test.txt")


def test_day09_part1(test_data):
    assert day09_part1(test_data) == 1928


def test_day09_part2(test_data):
    assert day09_part2(test_data) == 2858


if __name__ == "__main__":
    input_data = parse_input("data/day09.txt")

    print("Day 09 Part 1:")
    print(day09_part1(input_data))

    print("Day 09 Part 2:")
    print(day09_part2(input_data))
