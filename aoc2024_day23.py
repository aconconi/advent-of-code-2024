"""
Advent of Code 2024
Day 23: LAN Party
"""

from collections import defaultdict
from itertools import combinations

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        lines = data_file.read().splitlines()
    graph = defaultdict(list)
    for line in lines:
        a, b = line[:2], line[-2:]
        graph[a].append(b)
        graph[b].append(a)
    return graph


def bron_kerbosch(graph):
    cliques = []
    stack = [(set(), set(graph.keys()), set())]
    while stack:
        r, p, x = stack.pop()
        if not p and not x:
            cliques.append(r)
        else:
            for node in list(p):
                stack.append(
                    (
                        r.union({node}),
                        p.intersection(graph[node]),
                        x.intersection(graph[node]),
                    )
                )
                p.remove(node)
                x.add(node)
    return set(tuple(sorted(clique)) for clique in cliques)


def day23_part1(graph):
    connected_triads = {
        tuple(sorted([node, neighbor1, neighbor2]))
        for node, neighbors in graph.items()
        for neighbor1, neighbor2 in combinations(neighbors, 2)
        if neighbor2 in graph[neighbor1]
    }
    return sum(
        any(computer.startswith("t") for computer in triad)
        for triad in connected_triads
    )


def day23_part2(graph):
    cliques = bron_kerbosch(graph)
    return ",".join(max(cliques, key=len, default=[]))


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day23_test.txt")


def test_day23_part1(test_data):
    assert day23_part1(test_data) == 7


def test_day23_part2(test_data):
    assert day23_part2(test_data) == "co,de,ka,ta"


if __name__ == "__main__":
    input_data = parse_input("data/day23.txt")

    print("Day 23 Part 1:")
    print(day23_part1(input_data))

    print("Day 23 Part 2:")
    print(day23_part2(input_data))
