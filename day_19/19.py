import os
import functools

dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")

with open(file_path, 'r') as reader:
    lines = [line.rstrip('\n') for line in reader]


empty_index = lines.index('')
available_patterns = tuple(lines[:empty_index][0].split(', '))
target_towels = lines[empty_index + 1:]

@functools.lru_cache(None)
def can_make(target: str, options: tuple[str]) -> bool:
    if target == '':
        return True
    for option in options:
        if target.startswith(option):
            if can_make(target[len(option):], options):
                return True
    return False

count = 0
for target in target_towels:
    if can_make(target, available_patterns):
        count += 1
print(count) #part 1

#could just slightly modify can_make() but i want to keep part 1 and 2 separate

@functools.lru_cache(None)
def count_combinations(target: str, options: tuple[str]) -> int:
    if target == '':
        return 1
    combinations = 0
    for option in options:
        if target.startswith(option):
            combinations += count_combinations(target[len(option):], options)
    return combinations

count = 0
for target in target_towels:
    count += count_combinations(target, available_patterns)
print(count) #part 2