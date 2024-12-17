import os
import re
from collections import defaultdict

MAX_ROW = 103
MAX_COL = 101

dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")

with open(file_path, 'r') as reader:
    lines = [line.rstrip('\n') for line in reader]

def move(pos: tuple[int, int], vel: tuple[int, int]) -> tuple[int, int]:
    return ((pos[0] + vel[0]) % MAX_ROW, (pos[1] + vel[1]) % MAX_COL)

def calculate_safety_score(positions: defaultdict[tuple[int, int], int]) -> int:
    mid_row = MAX_ROW // 2
    mid_col = MAX_COL // 2
    quadrants = [0, 0, 0, 0]

    for (row, col), count in positions.items():
        if row == mid_row or col == mid_col:
            continue
        if row < mid_row and col < mid_col:
            quadrants[0] += count
        elif row < mid_row and col >= mid_col:
            quadrants[1] += count
        elif row >= mid_row and col < mid_col:
            quadrants[2] += count
        else:
            quadrants[3] += count

    return(quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3])

positions: defaultdict[tuple[int, int], int] = defaultdict(int)

robots = []
for line in lines:
    numbers = list(map(int, re.findall(r'-?\d+', line)))
    pos = (numbers[1], numbers[0])
    vel = (numbers[3], numbers[2])
    robots.append((pos, vel))

    for _ in range(100):
        pos = move(pos, vel)
    positions[pos] += 1

print(calculate_safety_score(positions))

step_data = []
for step in range(10000):
    positions = defaultdict(int)

    for i, (pos, vel) in enumerate(robots):
        pos = move(pos, vel)
        robots[i] = (pos, vel) 
        positions[pos] += 1

    safety_score = calculate_safety_score(positions)
    step_data.append((step, positions.copy(), safety_score))

step_data_sorted = sorted(step_data, key = lambda x: x[2])
lowest_scores = step_data_sorted[:100]

output_file_path = os.path.join(dir, "grids.txt")
with open(output_file_path, 'w') as f:
    for step, positions, safety_score in lowest_scores:
        f.write(f"Second: {step+1}\n")
        
        grid = [['.' for _ in range(MAX_ROW)] for _ in range(MAX_COL)]
        
        for (row, col), count in positions.items():
            if 0 <= col < MAX_ROW and 0 <= row < MAX_COL:
                grid[row][col] = '#'
        
        for row in grid:
            f.write(' '.join(row) + "\n")
        
        f.write("\n")