import os
from collections import deque

dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")

with open(file_path, 'r') as reader:
    lines = [line.rstrip('\n') for line in reader]

corrupted_coords = [(int(coord.split(',')[0]), int(coord.split(',')[1])) for coord in lines]

GRID_SIZE = 71

DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))

def is_in_bounds(pos: tuple[int, int]) -> bool:
    row, col = pos
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE

def make_grid(corrupted_coords: list[tuple[int, int]]) -> list[list[str]]:
    grid = []
    for row in range(GRID_SIZE):
        row_list = []
        for col in range(GRID_SIZE):
            if (col, row) in corrupted_coords[:1024]: 
                row_list.append('#')
            else:
                row_list.append('.')
        grid.append(row_list)

    return grid

def bfs(grid: list[list[str]], start: tuple[int, int], end: tuple[int, int]) -> int:
    q: deque[tuple[tuple[int, int], int]] = deque()
    q.append((start, 0))
    visited = {start}

    while q:
        (row, col), steps = q.popleft()

        if (row, col) == end:
            return steps
        
        for dr, dc in DIRS:
            next_row, next_col = row + dr, col + dc
            if is_in_bounds((next_row, next_col)) and (next_row, next_col) not in visited and grid[next_row][next_col] == '.':
                q.append(((next_row, next_col), steps + 1))
                visited.add((next_row, next_col))


    return -1


grid = make_grid(corrupted_coords)
start = (0, 0)
end = (GRID_SIZE - 1, GRID_SIZE - 1)

print(bfs(grid, start, end))

#part 2

for corrupted_coord in corrupted_coords[1025:]:
    crow, ccol = corrupted_coord
    grid[ccol][crow] = '#'
    if bfs(grid, start, end) == -1:
        print(corrupted_coord)
        break
