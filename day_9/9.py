import os
import numpy as np

dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")

with open(file_path, 'r') as reader:
    disk_map = reader.read().strip()

def get_blocks(disk_map: str) -> np.ndarray:
    result = []

    file_lengths = disk_map[::2]
    space_lengths = disk_map[1::2]

    file_id = 0
    for file_length, space_length in zip(file_lengths, space_lengths):
        result.extend([str(file_id)] * int(file_length))
        file_id += 1
        result.extend(['.'] * int(space_length))

    if len(file_lengths) > len(space_lengths):
        result.extend([str(file_id)] * int(file_lengths[-1]))
    else:
        result.extend(['.'] * int(space_lengths[-1]))
    
    return np.array(result)

def move_files(blocks: np.ndarray) -> np.ndarray:
    blocks = blocks.astype(str) 

    moved = True
    while moved:
        moved = False
        first_period_index = np.where(blocks == '.')[0][0] 
        
        for i in range(len(blocks) - 1, first_period_index, -1):
            if blocks[i] != '.':
                blocks[first_period_index], blocks[i] = blocks[i], blocks[first_period_index]
                moved = True
                break

    return blocks

import numpy as np

def move_whole_files(blocks: np.ndarray) -> np.ndarray:
    blocks = blocks.astype(str) 
    max_file_id = max(int(x) for x in blocks.flatten() if x != '.') 
    moved_files = set()  
    for file_id in range(max_file_id, 0, -1):
        file_id_str = str(file_id)
        
        file_positions = np.where(blocks == file_id_str)[0]
        
        if len(file_positions) == 0:
            continue 
        
        file_length = len(file_positions)
        
        free_space_groups = []
        start_index = -1
        free_space_length = 0
        
        for i in range(len(blocks)):
            if blocks[i] == '.':
                if start_index == -1:
                    start_index = i
                free_space_length += 1
            else:
                if free_space_length > 0:
                    free_space_groups.append((start_index, free_space_length))
                start_index = -1
                free_space_length = 0
        
        for start, length in free_space_groups:
            if length >= file_length and start < file_positions[0]:
                blocks[start:start+file_length] = file_id_str  
                blocks[file_positions[0]:file_positions[0]+file_length] = '.'  
                moved_files.add(file_id)
                break  
                
    return blocks

def checksum(files: np.ndarray) -> int:
    ans = 0 
    for i, char in enumerate(files):
        if char != '.':
            ans += (i * int(char))

    return ans

#part 1
ans = 0
blocks = get_blocks(disk_map)
moved_files = move_files(blocks)
print(checksum(moved_files))

#part 2
blocks = get_blocks(disk_map)
moved_whole_files = move_whole_files(blocks)
print(checksum(moved_whole_files))
