"""
Advent of Code 2024
Day 05: Print Queue
"""

from collections import defaultdict

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        edges, paths = data_file.read().strip().split("\n\n")
    edges = [line.split("|") for line in edges.splitlines()]
    rules = [(int(line[0]), int(line[1])) for line in edges]
    updates = [[int(x) for x in line.split(",")] for line in paths.splitlines()]
    sorted_updates = []
    for update in updates:
        order_map = build_order_map(rules, update)
        sorted_update = sorted(update, key=order_map.__getitem__)
        sorted_updates.append(sorted_update)

    return updates, sorted_updates


def topological_sort(graph: dict) -> list[int]:
    ans, temp, perm = [], set(), set()

    def visit(n):
        if n in perm:
            return
        if n in temp:
            raise ValueError("Graph has at least one cycle")

        temp.add(n)
        for m in graph.get(n, []):
            visit(m)
        temp.remove(n)
        perm.add(n)
        ans.append(n)

    for n in graph:
        if n not in perm:
            visit(n)

    return ans[::-1]


def build_order_map(rules: list[tuple[int, int]], update: list[int]) -> dict[int, int]:
    graph = defaultdict(list)
    for a, b in rules:
        if a in update and b in update:
            graph[a].append(b)
    return {node: idx for idx, node in enumerate(topological_sort(graph))}


def day05_part1(data):
    return sum(
        sorted_update[len(update) // 2]
        for update, sorted_update in zip(*data)
        if update == sorted_update
    )


def day05_part2(data):
    return sum(
        sorted_update[len(update) // 2]
        for update, sorted_update in zip(*data)
        if update != sorted_update
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day05_test.txt")


def test_day05_part1(test_data):
    assert day05_part1(test_data) == 143


def test_day05_part2(test_data):
    assert day05_part2(test_data) == 123


if __name__ == "__main__":
    input_data = parse_input("data/day05.txt")

    print("Day 05 Part 1:")
    print(day05_part1(input_data))

    print("Day 05 Part 2:")
    print(day05_part2(input_data))
