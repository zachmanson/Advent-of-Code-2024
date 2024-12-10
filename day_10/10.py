import os
dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")

with open(file_path, 'r') as reader:
    grid = [list(map(int, line.strip())) for line in reader]
 
DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))
MAX_X = len(grid[0])
MAX_Y= len(grid)

def is_in_bounds(pos: tuple[int, int]) -> bool:
    x, y = pos
    return 0 <= x < MAX_X and 0 <= y < MAX_Y

def get_neighbors(grid: list[list[int]], pos: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = pos
    val = grid[x][y]
    nbrs = []
    for dx, dy in DIRS:
        new_pos = (x + dx, y + dy)
        if is_in_bounds(new_pos) and grid[x + dx][y + dy] == val + 1:
            nbrs.append(new_pos)

    return nbrs

def get_trailhead_score(grid: list[list[int]], start: tuple[int, int]) -> int:
    visited = set()
    stack = [start]

    score = 0
    while stack:
        current = stack.pop()
        if current not in visited:
            if grid[current[0]][current[1]] == 9:
                score += 1
            visited.add(current)
            for neighbor in get_neighbors(grid, current):
                if neighbor not in visited:
                    stack.append(neighbor)

    return score


def get_trailhead_rating(grid: list[list[int]], start: tuple[int, int]) -> int:
    paths = set()
    stack = [(start, [start])] #current position, current path
    
    while stack:
        current, path = stack.pop()
        
        if grid[current[0]][current[1]] == 9:
            paths.add(tuple(path))
            continue
    
        for neighbor in get_neighbors(grid, current):
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor]))

    return len(paths)


starts = [(i, j) for i, row in enumerate(grid) for j, value in enumerate(row) if value == 0]
ans = sum(get_trailhead_score(grid, start) for start in starts)
print(ans)

ans_p2 = sum(get_trailhead_rating(grid, start) for start in starts)
print(ans_p2)

