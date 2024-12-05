from collections import defaultdict
from pprint import pp


def is_X_MAS(r, c, chars):
    mas = dict()
    count_ms = {"M": 0, "S": 0}
    for x in range(-1, 2):
        if x == 0:
            continue
        for y in range(-1, 2):
            if y == 0:
                continue
            current_char = chars[r + x][c + y]
            mas[f"{x}{y}"] = current_char
            if current_char in count_ms:
                count_ms[current_char] += 1
    return count_ms["M"] == 2 and count_ms["S"] == 2 and mas["-1-1"] != mas["11"]


def count_XMAS(line):
    count = 0
    XMAS = ["X", "M", "A", "S"]
    SMAX = ["S", "A", "M", "X"]
    current_char_idx = 0
    current_rev_idx = 0
    for idx, char in enumerate(line):
        if char == XMAS[current_char_idx]:
            current_char_idx += 1
            if current_char_idx > 3:
                count += 1
                current_char_idx = 0
        else:
            current_char_idx = 0 if char != XMAS[0] else 1
        if char == SMAX[current_rev_idx]:
            current_rev_idx += 1
            if current_rev_idx > 3:
                count += 1
                current_rev_idx = 0
        else:
            current_rev_idx = 0 if char != SMAX[0] else 1
    return count


def main():
    with open(file="./input", mode="r") as input_file:
        lines = input_file.read().splitlines()
    cols_count = len(lines)
    rows_count = len(lines[0])
    chars = list(map(lambda line: list(line), lines))

    #   -2-1 0 1 2
    # 0      00
    # 1    10  01
    # 2  20  11  02
    # 3    21  12
    # 4      22
    upright_diagonals = defaultdict(list)
    downright_diagonals = defaultdict(list)
    for r in range(rows_count):
        for c in range(cols_count):
            downright_diagonals[c - r].append(chars[r][c])
            upright_diagonals[c + r].append(chars[r][c])

    count_rows = sum(map(count_XMAS, chars))
    count_cols = sum(map(count_XMAS, zip(*chars)))  # transpose
    count_upr_diag = sum(map(count_XMAS, upright_diagonals.values()))
    count_dwr_diag = sum(map(count_XMAS, downright_diagonals.values()))

    total = count_rows + count_cols + count_upr_diag + count_dwr_diag

    print(f"count xmas: {total}")

    count_x_mas = 0
    for r in range(1, rows_count - 1):
        for c in range(1, cols_count - 1):
            if chars[r][c] == "A" and is_X_MAS(r, c, chars):
                count_x_mas += 1
    print(f"count X-mas: {count_x_mas}")


if __name__ == "__main__":
    main()
