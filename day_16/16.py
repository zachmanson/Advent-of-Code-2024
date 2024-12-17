import os
import heapq

dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")

with open(file_path, 'r') as reader:
    grid = [line.rstrip('\n') for line in reader]

#N: 0, E: 1, S: 2, W: 3
DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))

MAX_ROW = len(grid)
MAX_COL = len(grid[0])

def is_in_bounds(pos: tuple[int, int]) -> bool:
    row, col = pos
    return 0 <= row < MAX_ROW and 0 <= col < MAX_COL

start = (0, 0)
end = (0, 0)

for row in range(MAX_ROW):
    for col in range(MAX_COL):
        if grid[row][col] == 'S':
            start = (row, col)
        elif grid[row][col] == 'E':
            end = (row, col)

def dijkstra(grid: list[str], start: tuple[int, int]) -> tuple[dict, dict]:
    start_state = (start[0], start[1], 1)

    pq = []
    heapq.heappush(pq, (0, start_state))  
    visited = {start_state: 0}
    prev = {}

    while pq:
        cost, (row, col, dir_idx) = heapq.heappop(pq)  

        if visited.get((row, col, dir_idx), float('inf')) < cost:
            continue

        dr, dc = DIRS[dir_idx]
        next_row, next_col = row + dr, col + dc
        if is_in_bounds((next_row, next_col)) and grid[next_row][next_col] != '#':
            new_cost = cost + 1
            if new_cost < visited.get((next_row, next_col, dir_idx), float('inf')):
                visited[(next_row, next_col, dir_idx)] = new_cost
                prev[(next_row, next_col, dir_idx)] = []
                
            if new_cost == visited.get((next_row, next_col, dir_idx), float('inf')):
                prev[(next_row, next_col, dir_idx)].append((row, col, dir_idx))
                heapq.heappush(pq, (new_cost, (next_row, next_col, dir_idx))) 
        for new_dir_idx in [(dir_idx - 1) % 4, (dir_idx + 1) % 4]:
            new_cost = cost + 1000  
            if new_cost < visited.get((row, col, new_dir_idx), float('inf')):
                visited[(row, col, new_dir_idx)] = new_cost
                prev[(row, col, new_dir_idx)] = []
            if new_cost == visited.get((row, col, new_dir_idx), float('inf')):
                prev[(row, col, new_dir_idx)].append((row, col, dir_idx))
                heapq.heappush(pq, (new_cost, (row, col, new_dir_idx))) 

    return visited, prev
    
def backtrack(visited: dict, prev: dict, start: tuple[int, int], end: tuple[int, int]) -> set:
    path = set()
    min_cost = min(visited.get((end[0], end[1], d), float('inf')) for d in range(4))

    end_states = [
        (end[0], end[1], dir_idx)
        for dir_idx in range(4)
        if visited.get((end[0], end[1], dir_idx), float('inf')) == min_cost
    ]

    stack = []
    visited_backtrack = set() 
    for end_state in end_states:
        stack.append(end_state)
        visited_backtrack.add(end_state)
    
    while stack:
        current_state = stack.pop()
        if current_state is None:
            continue
        if current_state == (start[0], start[1], 1):
            path.add((current_state[0], current_state[1]))
            continue

        path.add((current_state[0], current_state[1]))
        
        for next_state in prev.get(current_state, []):
            if next_state not in visited_backtrack:
                stack.append(next_state)
                visited_backtrack.add(next_state)
            
    return path

#part 1 
visited, prev = dijkstra(grid, start)
print(min(visited.get((end[0], end[1], d), float('inf')) for d in range(4)))

#part 2
best_paths = backtrack(visited, prev, start, end)
print(len(best_paths))