from sympy import symbols, Eq, solve
from pprint import pp
import re


def read_file(path):
    with open(file=path, mode="r") as input_file:
        lines = input_file.read()
    return lines


def parse_input(lines):
    pattern = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    results = re.findall(pattern, lines)
    equations = []
    for result in results:
        equation = tuple(map(int, result))
        equations.append(equation)
    return equations


def solve_sympy(equation):
    ax, ay, bx, by, px, py = equation
    px += 10000000000000
    py += 10000000000000
    a, b = symbols('a b', integer=True)
    eq1 = Eq(ax * a + bx * b, px)
    eq2 = Eq(ay * a + by * b, py)

    solution = solve((eq1, eq2), (a, b))
    if solution: 
        return solution[a] * 3 + solution[b]
    else:
        return 0


def solve_myself(equation):
    """
    94 * a + 22 * b = 8400
    34 * a + 67 * b = 5400
    substitution
    b = (8400 - 94 * a) // 22
    34 * a + 67 * ((8400 - 94 * a) // 22) = 5400
    34 * a + (67 * 8400 - 67 * 94 * a) // 22 = 5400
    22 * 34 * a + 67 * 8400 - 67 * 94 * a = 22 * 5400
    748 * a + 562800 - 6298 * a = 118800
    (748 - 6298) * a = 118800 - 562800
    -5550 * a = -444000
    a = 80
    94 * 80 + 22 * b = 8400
    22 * b = 8400 - 7520
    b = 880 // 22
    b = 40

    ax * a + bx * b = px
    ay * a + by * b = py
    substitution
    b = (px - ax * a) // bx
    ay * a + by * ((px - ax * a) // bx) = py
    bx * ay * a + by * px - by * ax * a = bx * py
    bx * ay * a           - by * ax * a = bx * py - by * px
    (bx * ay - by * ax) * a = bx * py - by * px
    a = (bx * py - by * px) // (bx * ay - by * ax)
    """
    ax, ay, bx, by, px, py = equation
    px += 10000000000000
    py += 10000000000000
    a = (bx * py - by * px) // (bx * ay - by * ax)
    b = (px - ax * a) // bx

    if (ax * a + bx * b == px) and (ay * a + by * b == py):
        return a * 3 + b
    else:
        return 0


def main():
    lines = read_file("./input")
    equations = parse_input(lines)
    total = 0
    for equation in equations:
        total += solve_myself(equation)
    pp(total)


if __name__ == "__main__":
    main()
