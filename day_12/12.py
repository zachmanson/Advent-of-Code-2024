import os
from collections import deque
dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")

with open(file_path, 'r') as reader:
    grid = [line.rstrip('\n') for line in reader]
 
DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))

MAX_COL = len(grid[0])
MAX_ROW= len(grid)

def is_in_bounds(pos: tuple[int, int]) -> bool:
    row, col = pos
    return 0 <= row < MAX_ROW and 0 <= col < MAX_COL

def find_region(grid: list[str], start: tuple[int, int], visited: set[tuple[int, int]]) -> tuple[int, int, set[tuple[int, int]]]:
    letter = grid[start[0]][start[1]]
    queue = deque([start])
    visited.add(start)
    area = 0
    perimeter = 0

    while queue:
        row, col = queue.popleft()
        area += 1

        for dr, dc in DIRS:
            nr, nc = row + dr, col + dc
            if not is_in_bounds((nr, nc)) or grid[nr][nc] != letter:
                perimeter += 1
            elif (nr, nc) not in visited and grid[nr][nc] == letter:
                visited.add((nr, nc))
                queue.append((nr, nc))

    return area, perimeter, visited

def find_region_whole_sides(grid: list[str], start: tuple[int, int], visited: set[tuple[int, int]]) -> tuple[int, int, set[tuple[int, int]]]:
    letter = grid[start[0]][start[1]]
    queue = deque([start])
    region = set()  

    while queue:
        row, col = queue.popleft()
        if (row, col) in visited:
            continue

        visited.add((row, col))
        region.add((row, col))

        for dr, dc in DIRS:
            nr, nc = row + dr, col + dc
            if is_in_bounds((nr, nc)) and grid[nr][nc] == letter:
                queue.append((nr, nc))

    perimeter, shared_borders = 0, 0
    for row, col in region:
        # up
        if not is_in_bounds((row - 1, col)) or grid[row - 1][col] != letter:
            perimeter += 1
            if is_in_bounds((row, col - 1)) and grid[row][col - 1] == letter and (not is_in_bounds((row - 1, col - 1)) or grid[row - 1][col - 1] != letter):
                shared_borders += 1
        # down
        if not is_in_bounds((row + 1, col)) or grid[row + 1][col] != letter:
            perimeter += 1
            if is_in_bounds((row, col - 1)) and grid[row][col - 1] == letter and (not is_in_bounds((row + 1, col - 1)) or grid[row + 1][col - 1] != letter):
                shared_borders += 1
        # left
        if not is_in_bounds((row, col - 1)) or grid[row][col - 1] != letter:
            perimeter += 1
            if is_in_bounds((row - 1, col)) and grid[row - 1][col] == letter and (not is_in_bounds((row - 1, col - 1)) or grid[row - 1][col - 1] != letter):
                shared_borders += 1
        # right
        if not is_in_bounds((row, col + 1)) or grid[row][col + 1] != letter:
            perimeter += 1
            if is_in_bounds((row - 1, col)) and grid[row - 1][col] == letter and (not is_in_bounds((row - 1, col + 1)) or grid[row - 1][col + 1] != letter):
                shared_borders += 1

    total_sides = perimeter - shared_borders
    return len(region), total_sides, visited


#part 1
price = 0
visited: set[tuple[int, int]] = set()
for row in range(MAX_ROW):
    for col in range(MAX_COL):
        if (row, col) not in visited:
            area, perimeter, visited = find_region(grid, (row, col), visited)
            price += (area * perimeter)
print(price)

#part 2
price = 0
visited: set[tuple[int, int]] = set()
for row in range(MAX_ROW):
    for col in range(MAX_COL):
        if (row, col) not in visited:
            area, sides, visited = find_region_whole_sides(grid, (row, col), visited)
            price += (area * sides)
print(price)
