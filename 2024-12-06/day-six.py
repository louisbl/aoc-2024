from collections import defaultdict
from curses import wrapper
from pprint import pp
from enum import Enum


class Directions(Enum):
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"


class Mark(Enum):
    VERTICAL = "|"
    HORIZONTAL = "-"
    CROSS = "+"
    OBSTACLE = "0"


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.x}_{self.y}"


class Guard:
    def __init__(self, point, direction) -> None:
        self.position = point
        self.direction = direction

    def set_position(self, point):
        self.position.x = point.x
        self.position.y = point.y

    def __repr__(self) -> str:
        return f"{self.position}_{self.direction.name}"


class Carto:
    def __init__(self, lines) -> None:
        self.lines = lines
        self.reset()
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.loops = 0

    def reset(self):
        self.map = list(map(lambda line: list(line), self.lines))


INIT_POINT = Point(0, 0)
LINES = None


def read_file(path):
    with open(file=path, mode="r") as input_file:
        lines = input_file.read().splitlines()
    return lines


def display_carto(stdscr, carto, positions_visited):
    for y, row in enumerate(carto.map):
        for x, cell in enumerate(row):
            stdscr.addstr(y, x, cell)
    stdscr.addstr(carto.height, 0, f"visited: {len(positions_visited)}")
    stdscr.addstr(carto.height + 1, 0, f"loops: {carto.loops}")
    stdscr.getch()


def move_guard(stdscr, carto, guard):
    positions_visited = defaultdict(str)
    guard_trail = defaultdict(set)
    next_position = Point(guard.position.x, guard.position.y)
    guard_in_bounds = True
    is_looping = False

    while guard_in_bounds and not is_looping:
        match guard.direction:
            case Directions.UP:
                next_position.y -= 1
            case Directions.RIGHT:
                next_position.x += 1
            case Directions.DOWN:
                next_position.y += 1
            case Directions.LEFT:
                next_position.x -= 1

        previous_direction = guard.direction
        previous_position = Point(guard.position.x, guard.position.y)

        if -1 < next_position.x < carto.width and -1 < next_position.y < carto.height:
            while (
                carto.map[next_position.y][next_position.x] == "#"
                or carto.map[next_position.y][next_position.x] == "O"
            ) and not is_looping:
                if carto.loops == 29:
                    pass
                match guard.direction:
                    case Directions.UP:
                        next_position.y += 1
                        guard.direction = Directions.RIGHT
                        next_position.x += 1
                    case Directions.RIGHT:
                        next_position.x -= 1
                        guard.direction = Directions.DOWN
                        next_position.y += 1
                    case Directions.DOWN:
                        next_position.y -= 1
                        guard.direction = Directions.LEFT
                        next_position.x -= 1
                    case Directions.LEFT:
                        next_position.x += 1
                        guard.direction = Directions.UP
                        next_position.y -= 1

                if guard.direction.value in guard_trail[repr(next_position)]:
                    is_looping = True

        else:
            guard_in_bounds = False

        guard.set_position(next_position)

        mark = Mark.CROSS
        if previous_direction == guard.direction:
            mark = (
                Mark.VERTICAL
                if guard.direction == Directions.UP
                or guard.direction == Directions.DOWN
                else Mark.HORIZONTAL
            )

        if repr(previous_position) in positions_visited.keys():
            mark = Mark.CROSS

        positions_visited[repr(previous_position)] = mark.value
        carto.map[previous_position.y][previous_position.x] = mark.value
        guard_trail[repr(guard.position)].add(guard.direction.value)
        if guard_in_bounds:
            carto.map[guard.position.y][guard.position.x] = guard.direction.value

        if stdscr:
            display_carto(stdscr, carto, positions_visited)

    return positions_visited, is_looping


def find_obstructions(stdscr, carto, visited, initial_point):
    for pos_str, value in visited.items():
        position = pos_str.split("_")
        carto.reset()
        old_value = carto.map[int(position[1])][int(position[0])]
        carto.map[int(position[1])][int(position[0])] = "O"
        visited, is_looping = move_guard(
            stdscr, carto, Guard(Point(initial_point.x, initial_point.y), Directions.UP)
        )
        if is_looping:
            carto.loops += 1
        carto.map[int(position[1])][int(position[0])] = old_value

        if stdscr:
            display_carto(stdscr, carto, visited)


def find_guard(carto):
    for y, row in enumerate(carto.map):
        for x, cell in enumerate(row):
            if cell == "^":
                return Guard(Point(x, y), Directions.UP)


def main(stdscr):
    if stdscr:
        stdscr.clear()

    lines = read_file("./input")
    carto = Carto(lines)
    guard = find_guard(carto)
    initial_point = Point(guard.position.x, guard.position.y)

    visited, _ = move_guard(stdscr, carto, guard)
    find_obstructions(stdscr, carto, visited, initial_point)

    if stdscr:
        stdscr.addstr(0, 0, f"visited: {len(visited)}")
        stdscr.addstr(1, 0, f"loops: {carto.loops}")
        stdscr.addstr(2, 0, "press q to quit")
        while True:
            if stdscr.getch() == ord("q"):
                break
    else:
        pp(f"visited: {len(visited)}")
        pp(f"loops: {carto.loops}")


if __name__ == "__main__":
    # wrapper(main)
    main(None)
