import os
dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")

with open(file_path, 'r') as reader:
    lines = [line.rstrip('\n') for line in reader]

safe = 0
for line in lines:
    report = [int(x) for x in line.split()]
    is_increasing = all(x < y for x, y in zip(report, report[1:]))
    is_decreasing = all(x > y for x, y in zip(report, report[1:]))
    if is_increasing or is_decreasing:
        if all(1 <= abs(x - y) <= 3 for x, y in zip(report, report[1:])):
            safe += 1

print(safe) #part 1


safe = 0
for line in lines:
    report = [int(x) for x in line.split()]
    violation_count = 0

    for i in range(len(report) - 1):
        if not (1 <= abs(report[i] - report[i + 1]) <= 3):
            violation_count += 1

    if violation_count > 2:
        continue

    for i in range(len(report)):
        new_report = report[:i] + report[i+1:]
        is_increasing = all(x < y for x, y in zip(new_report, new_report[1:]))
        is_decreasing = all(x > y for x, y in zip(new_report, new_report[1:]))
        if is_increasing or is_decreasing:
            if all(1 <= abs(x - y) <= 3 for x, y in zip(new_report, new_report[1:])):
                safe += 1 
                break

print(safe)