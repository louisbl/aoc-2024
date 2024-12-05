from collections import defaultdict
from functools import cmp_to_key


def read_file(path):
    with open(file=path, mode="r") as input_file:
        lines = input_file.read().splitlines()
    return lines


def get_rules(lines):
    rules = []
    for line in lines[:]:
        lines.remove(line)
        if line == "":
            break
        rules.append(line)
    return rules


def get_updates(lines):
    return list(map(lambda line: line.split(","), lines))


def parse_rules(rules_raw):
    rules = defaultdict(set)
    for rule in rules_raw:
        before, after = rule.split("|")
        rules[before].add(after)
    return rules


def is_unordered(rules, pages):
    for idx, page in enumerate(pages):
        before = pages[:idx]
        for page_before in before:
            if page_before in rules[page]:
                return True
    return False


def check_rules(rules, updates):
    ordered = updates[:]
    unordered = []
    for pages in updates:
        if is_unordered(rules, pages):
            ordered.remove(pages)
            unordered.append(pages)

    return ordered, unordered


def sum_middle_page(pages):
    return sum(map(lambda pages: int(pages[len(pages) // 2]), pages))


def order_pages(rules, updates):
    ordered = []

    def compare(a, b):
        return 1 if a in rules[b] else -1

    for pages in updates:
        ordered.append(sorted(pages, key=cmp_to_key(compare)))
    return ordered


def main():
    lines = read_file("./input")
    rules_raw = get_rules(lines)
    updates = get_updates(lines)
    rules = parse_rules(rules_raw)

    updates_ordered, updates_unordered = check_rules(rules, updates)
    total_ordered = sum_middle_page(updates_ordered)
    print(f"part one: {total_ordered}")

    updates_changed = order_pages(rules, updates_unordered)
    total_unordered = sum_middle_page(updates_changed)
    print(f"part two: {total_unordered}")


if __name__ == "__main__":
    main()
