from pprint import pp


def read_file(path):
    with open(file=path, mode="r") as input_file:
        line = input_file.read().strip()
    return line


def expand(line):
    blocks = []
    file_id = 0
    for idx, block in enumerate(line):
        is_file = idx % 2 == 0
        if is_file:
            for count in range(int(block)):
                blocks.append(file_id)
            file_id += 1
        else:
            for count in range(int(block)):
                blocks.append(-1)
    return blocks


def compact(blocks):
    compacted = blocks[:]
    for block in reversed(compacted):
        compacted.pop()
        if block != -1:
            new_index = 0
            while True:
                if new_index == len(compacted):
                    compacted.append(block)
                    return compacted
                if compacted[new_index] != -1:
                    new_index += 1
                else:
                    break
            compacted[new_index] = block


def find_checksum(blocks):
    total = 0
    for idx, block in enumerate(blocks):
        total += idx * int(block)
    return total


def main():
    line = read_file("./input")
    blocks = expand(list(line))
    compacted = compact(blocks)
    checksum = find_checksum(compacted)
    pp(checksum)


if __name__ == "__main__":
    main()
