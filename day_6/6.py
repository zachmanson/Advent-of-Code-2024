import os
dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")
with open(file_path, 'r') as reader:
    grid = [line.rstrip('\n') for line in reader]

MAX_X = len(grid[0])
MAX_Y = len(grid)

RIGHT: dict[tuple, tuple] = {
    (-1, 0): (0, 1),  # up -> right
    (0, 1): (1, 0),   # right -> down
    (1, 0): (0, -1),  # down -> left
    (0, -1): (-1, 0)  # left -> up
}

def find_start(grid: list[str]) -> tuple[int, int]:
    for row, line in enumerate(grid):
        col = line.find('^')
        if col != -1:
            return (row, col) 
    return None

def is_in_bounds(coords: tuple[int, int]) -> bool:
    row, col = coords
    return 0 <= row < MAX_Y and 0 <= col < MAX_X


def get_guard_path(grid: list[str], start_pos: tuple[int, int]) -> set[tuple[int, int]]:
    start_dir = (-1, 0)  
    path = set()  
    current_pos = start_pos
    current_dir = start_dir

    while True:
        path.add(current_pos)

        next_pos = (current_pos[0] + current_dir[0], current_pos[1] + current_dir[1])
        
        if not is_in_bounds(next_pos):
            break 
        
        row, col = next_pos
        if grid[row][col] == '#': 
            current_dir = RIGHT[current_dir]  
        else:
            current_pos = next_pos  

    return path

start_pos = find_start(grid)
path = get_guard_path(grid, start_pos)
print(len(path))

#part 2

def has_loop(grid: list[str], start_pos: tuple[int, int]) -> bool:
    start_dir = (-1, 0)
    visited = set()
    current_pos = start_pos
    current_dir = start_dir

    while True:
        if (current_pos, current_dir) in visited:
            return True
        
        visited.add((current_pos, current_dir))

        next_pos = (current_pos[0] + current_dir[0], current_pos[1] + current_dir[1])
        
        if not is_in_bounds(next_pos):
            return False
        
        row, col = next_pos
        if grid[row][col] == '#':
            current_dir = RIGHT[current_dir]
        else:
            current_pos = next_pos

def place_obstruction(grid: list[str], position: tuple[int, int]) -> list[str]:
    new_grid = [list(row) for row in grid]
    row, col = position
    new_grid[row][col] = '#'
    return [''.join(row) for row in new_grid]

count = 0
visited_positions = set()

start_pos = find_start(grid)
guard_path = get_guard_path(grid, start_pos)

for coords in guard_path:
    if coords not in visited_positions: 
        new_grid = place_obstruction(grid, coords)
        if has_loop(new_grid, start_pos):
            count += 1
        visited_positions.add(coords)

print(count)
