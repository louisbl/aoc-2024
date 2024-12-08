from concurrent.futures import ProcessPoolExecutor
import operator
import itertools


def concatenate(a, b):
    return int(str(a) + str(b))


operators = [operator.add, operator.mul, concatenate]


def read_file(path):
    with open(file=path, mode="r") as input_file:
        lines = input_file.read().splitlines()
    return lines


def resolve_equation(expected, operands, operations):
    result = int(operands[0])
    for idx, operation in enumerate(operations, 1):
        result = operation(result, int(operands[idx]))
        if result == expected:
            return True
    return False


def is_equation_true(equation):
    expected = equation[0]
    operands = equation[1:]
    for operations in itertools.product(operators, repeat=len(operands) - 1):
        if resolve_equation(expected, operands, operations):
            return expected
    return 0


def main():
    lines = read_file("./input")
    operations_raw = map(lambda line: line.split(":"), lines)
    operations = list(
        map(
            lambda operation: [int(operation[0]), *operation[1].split()], operations_raw
        )
    )
    with ProcessPoolExecutor() as executor:
        total = sum(executor.map(is_equation_true, operations))
        print(total)


if __name__ == "__main__":
    main()
