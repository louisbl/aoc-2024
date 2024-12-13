from collections import defaultdict
import itertools
from pprint import pp


def in_bounds(grid, node):
    x, y = node
    return -1 < x < len(grid[0]) and -1 < y < len(grid)


def find_antinodes(antennas, grid):
    antinodes = set()
    for frequency, positions in antennas.items():
        antinodes.update(positions)
        for (ax, ay), (bx, by) in itertools.combinations(positions, r=2):
            dx = bx - ax
            dy = by - ay
            i = 0
            while True:
                i += 1
                node = (ax - i * dx, ay - i * dy)
                if in_bounds(grid, node):
                    antinodes.add(node)
                else:
                    break
            i = 0
            while True:
                i += 1
                node = (bx + i * dx, by + i * dy)
                if in_bounds(grid, node):
                    antinodes.add(node)
                else:
                    break

    return antinodes


def find_antennas(grid):
    antennas = defaultdict(set)
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell != ".":
                antennas[cell].add((x, y))
    return antennas


def read_file(path):
    with open(file=path, mode="r") as input_file:
        lines = input_file.read().splitlines()
    return lines


def main():
    lines = read_file("./input")
    grid = list(map(lambda line: list(line), lines))
    antennas = find_antennas(grid)
    antinodes = find_antinodes(antennas, grid)
    pp(len(antinodes))


if __name__ == "__main__":
    main()
