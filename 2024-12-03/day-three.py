import re


def filter(input):
    values = re.findall(r"(don\'t)|(do)|mul\(([0-9]{1,3}\,[0-9]{1,3})\)", input)
    operations = []
    is_doing = True
    for value in values:
        (dont, do, mul) = value
        if is_doing:
            is_doing = dont == ""
        else:
            is_doing = do == "do"
        if is_doing and mul != "":
            operations.append(mul)
    return operations


def main():
    input = ""

    with open(file="./input", mode="r") as input_file:
        for line in input_file:
            input += line
    operations = filter(input)
    total = 0
    for operation in operations:
        operands = operation.split(",")
        mul = int(operands[0]) * int(operands[1])
        total += mul

    print(f"operations: {operations}")
    print(f"total: {total}")


if __name__ == "__main__":
    main()
