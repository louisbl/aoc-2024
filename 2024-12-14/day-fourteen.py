import math
from pprint import pp
from PIL import Image

GRID_WIDTH = 101
GRID_HEIGHT = 103


class Robot:
    def __init__(self, position, velocity):
        [x, y] = position
        self.position = (int(x), int(y))
        [vx, vy] = velocity
        self.velocity = (int(vx), int(vy))

    def __repr__(self):
        return "*"


def read_file(path):
    with open(file=path, mode="r") as input_file:
        lines = input_file.read().splitlines()
    return lines


def parse_input(lines):
    robots = set()
    for line in lines:
        info = line.split()
        position = info[0][2:].split(",")
        velocity = info[1][2:].split(",")
        robot = Robot(position, velocity)
        robots.add(robot)
    return robots


def init_grid(w, h):
    grid = []
    for y in range(h):
        row = []
        for x in range(w):
            row.append(set())
        grid.append(row)
    return grid


def add_robots(grid, robots):
    for robot in robots:
        (x, y) = robot.position
        grid[y][x].add(robot)


def move(grid, robot):
    (x, y) = robot.position
    grid[y][x].remove(robot)
    (vx, vy) = robot.velocity
    new_x = (x + vx) % GRID_WIDTH
    new_y = (y + vy) % GRID_HEIGHT
    robot.position = (new_x, new_y)
    grid[new_y][new_x].add(robot)


def show_grid(grid, step, safety):
    image = Image.new("RGB", (GRID_WIDTH, GRID_HEIGHT))
    pixels = image.load()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if len(cell) > 0:
                pixels[x, y] = (255, 255, 255)
            else:
                pixels[x, y] = (0, 0, 0)
    image.save(f"./img/{safety}_{step}.bmp")


def main():
    lines = read_file("./input")
    robots = parse_input(lines)
    grid = init_grid(GRID_WIDTH, GRID_HEIGHT)
    add_robots(grid, robots)
    for step in range(1, 10001):
        for robot in robots:
            move(grid, robot)
        safety_factor = calc_safety(grid)
        if step == 100:
            pp(safety_factor)
        show_grid(grid, step, safety_factor)


def calc_safety(grid):
    quadrants = [
        (0, 0),
        (GRID_WIDTH // 2 + 1, 0),
        (0, GRID_HEIGHT // 2 + 1),
        (GRID_WIDTH // 2 + 1, GRID_HEIGHT // 2 + 1),
    ]
    counts = []
    for top_x, top_y in quadrants:
        count = 0
        for x in range(top_x, top_x + GRID_WIDTH // 2):
            for y in range(top_y, top_y + GRID_HEIGHT // 2):
                count += len(grid[y][x])
        counts.append(count)
    safety_factor = math.prod(counts)
    return safety_factor


if __name__ == "__main__":
    main()
