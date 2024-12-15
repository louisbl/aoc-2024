from collections import defaultdict, deque
from pprint import pp


def read_file(path):
    with open(file=path, mode="r") as input_file:
        lines = input_file.read().splitlines()
    return lines


def in_bounds(grid, node):
    x, y = node
    return -1 < x < len(grid[0]) and -1 < y < len(grid)


def get_adjacents(position):
    x, y = position
    up = (x, y - 1)
    right = (x + 1, y)
    down = (x, y + 1)
    left = (x - 1, y)
    adjacents = [up, right, down, left]
    return adjacents


def search(grid, visited, position, plant):
    queue = deque()
    region = set()

    queue.append(position)

    while queue:
        position = queue.popleft()
        neighbours = 0
        for adjacent in get_adjacents(position):
            x, y = adjacent
            if in_bounds(grid, adjacent) and grid[y][x] == plant:
                neighbours += 1
                if adjacent not in visited:
                    visited.add(adjacent)
                    queue.append(adjacent)
        region.add((position, 4 - neighbours))
    return region


def find_regions(grid):
    visited = set()
    regions = defaultdict(list)

    for y, row in enumerate(grid):
        for x, plant in enumerate(row):
            position = (x, y)
            if position not in visited:
                visited.add(position)
                region = search(grid, visited, position, plant)
                regions[plant].append(region)
    return regions


def calc_cost(regions):
    total = 0
    for region, groups in regions.items():
        for group in groups:
            area = 0
            perimeter = 0
            for position, fences in group:
                area += 1
                perimeter += fences
            cost = area * perimeter
            total += cost
    return total


def main():
    lines = read_file("./input")
    grid = [list(line) for line in lines]
    regions = find_regions(grid)
    total = calc_cost(regions)
    pp(total)


if __name__ == "__main__":
    main()
