"""
Advent of Code 2024
Day 23:
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


def find_fully_connected_triads(graph):
    return {
        tuple(sorted([node, neighbor1, neighbor2]))
        for node, neighbors in graph.items()
        for neighbor1, neighbor2 in combinations(neighbors, 2)
        if neighbor2 in graph[neighbor1]
    }


def find_cliques(graph):
    cliques = []

    def bron_kerbosch(r, p, x):
        if not p and not x:
            cliques.append(r)
        for node in list(p):
            bron_kerbosch(
                r.union({node}),
                p.intersection(graph[node]),
                x.intersection(graph[node]),
            )
            p.remove(node)
            x.add(node)

    bron_kerbosch(set(), set(graph.keys()), set())
    return set(tuple(sorted(c)) for c in cliques)


def day23_part1(graph):
    return sum(
        any(computer[0] == "t" for computer in triad)
        for triad in find_fully_connected_triads(graph)
    )


def day23_part2(graph):
    cliques = find_cliques(graph)
    if cliques:
        max_clique = max(cliques, key=len) if cliques else []
        return ",".join(sorted(max_clique))


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
    print(day23_part1(input_data))  # Correct answer is 1184

    print("Day 23 Part 2:")
    print(
        day23_part2(input_data)
    )  # Correct answer is "hf,hz,lb,lm,ls,my,ps,qu,ra,uc,vi,xz,yv"
