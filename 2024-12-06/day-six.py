import curses
from curses import wrapper
from pprint import pp
from enum import Enum


class Directions(Enum):
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class Guard:
    def __init__(self, point, direction) -> None:
        self.point = point
        self.direction = direction

    def set_position(self, point):
        self.point.x = point.x
        self.point.y = point.y

    def get_position(self):
        return f"{self.point.x}_{self.point.y}"


class Carto:
    def __init__(self, lines) -> None:
        self.map = list(map(lambda line: list(line), lines))
        self.height = len(self.map)
        self.width = len(self.map[0])


def read_file(path):
    with open(file=path, mode="r") as input_file:
        lines = input_file.read().splitlines()
    return lines


def display_carto(stdscr, carto, positions_visited):
    for y, row in enumerate(carto.map):
        for x, cell in enumerate(row):
            stdscr.addstr(y, x, cell)
    stdscr.addstr(carto.height, 0, f'visited: {len(positions_visited)}')
    stdscr.getch()


def move_guard(stdscr, carto, guard):
    positions_visited = set()
    positions_visited.add(guard.get_position())
    next_position = Point(guard.point.x, guard.point.y)
    guard_in_bounds = True

    while guard_in_bounds:
        # display_carto(stdscr, carto, positions_visited)
        match guard.direction:
            case Directions.UP:
                next_position.y -= 1
            case Directions.RIGHT:
                next_position.x += 1
            case Directions.DOWN:
                next_position.y += 1
            case Directions.LEFT:
                next_position.x -= 1
        if -1 < next_position.x < carto.width and -1 < next_position.y < carto.height:
            cell = carto.map[next_position.y][next_position.x]
            # check if cell already visited and an intersection, in this case put an obstacle in next position
            # check guard is looping and try again
            if cell == "#":
                match guard.direction:
                    case Directions.UP:
                        next_position.y += 1
                        guard.direction = Directions.RIGHT
                    case Directions.RIGHT:
                        next_position.x -= 1
                        guard.direction = Directions.DOWN
                    case Directions.DOWN:
                        next_position.y -= 1
                        guard.direction = Directions.LEFT
                    case Directions.LEFT:
                        next_position.x += 1
                        guard.direction = Directions.UP
            else:
                carto.map[guard.point.y][guard.point.x] = "X"
                guard.set_position(next_position)
                carto.map[guard.point.y][guard.point.x] = guard.direction.value
                positions_visited.add(guard.get_position())
        else:
            guard_in_bounds = False


def find_guard(carto):
    for y, row in enumerate(carto.map):
        for x, cell in enumerate(row):
            if cell == "^":
                return Guard(Point(x, y), Directions.UP)


def main(stdscr):
    stdscr.clear()
    lines = read_file("./input")
    carto = Carto(lines)
    guard = find_guard(carto)
    move_guard(stdscr, carto, guard)


if __name__ == "__main__":
    wrapper(main)
