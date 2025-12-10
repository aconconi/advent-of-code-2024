"""
Advent of Code 2024
Day 02: Red-Nosed Reports
"""

from itertools import pairwise

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return [tuple(map(int, report.split())) for report in data_file]


def is_report_safe(report):
    levels = report if report[0] <= report[-1] else reversed(report)
    return all(1 <= (b - a) <= 3 for a, b in pairwise(levels))


def day02_part1(data):
    return sum(is_report_safe(report) for report in data)


def day02_part2(data):
    def gen_sub_reports(report):
        for i in range(len(report) + 1):
            yield report[:i] + report[i + 1 :]

    return sum(
        any(is_report_safe(sub_report) for sub_report in gen_sub_reports(report))
        for report in data
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day02_test.txt")


def test_day02_part1(test_data):
    assert day02_part1(test_data)


def test_day02_part2(test_data):
    assert day02_part2(test_data)


if __name__ == "__main__":
    input_data = parse_input("data/day02.txt")

    print("Day 02 Part 1:")
    print(day02_part1(input_data))

    print("Day 02 Part 2:")
    print(day02_part2(input_data))
