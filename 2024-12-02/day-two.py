def check_safety(report):
    diff = 0
    previous_levels = None
    is_ascending = True
    is_descending = True
    for idx, current_levels in enumerate(report):
        if idx == 0:
            previous_levels = current_levels
            continue

        diff = current_levels - previous_levels

        if diff == 0:
            return False

        is_in_bounds = 1 <= abs(diff) <= 3
        if not is_in_bounds:
            return False

        if diff > 0:
            is_descending = False
        elif diff < 0:
            is_ascending = False

        if is_ascending or is_descending:
            previous_levels = current_levels
        else:
            return False

    return True


def main():
    reports = []

    with open(file="./input", mode="r") as input_file:
        for line in input_file:
            reports.append(list(map(int, line.split())))

    print(f"count: {len(reports)}")

    reports_safe = 0
    reports_damp_safe = 0
    for report in reports:
        if check_safety(report):
            reports_safe += 1
        else:
            for idx in range(len(report)):
                damp_report = report[:idx] + report[idx + 1 :]
                if check_safety(damp_report):
                    reports_damp_safe += 1
                    break

    print(f"reports safe: {reports_safe}")
    print(f"reports damp safe: {reports_damp_safe}")
    print(f"reports total safe: {reports_safe + reports_damp_safe}")

if __name__ == "__main__":
    main()
