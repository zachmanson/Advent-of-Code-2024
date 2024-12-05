import os
dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")
from collections import deque


with open(file_path, 'r') as reader:
    lines = [line for line in reader]

newline = lines.index('\n')
page_order = [line.rstrip('\n') for line in lines[:newline]]
page_numbers = [line.rstrip('\n') for line in lines[newline + 1:]]

order: dict[int, list[int]] = {}

for pages in page_order:
    first_page, second_page = [int(x) for x in pages.split('|')]
    if second_page not in order:
        order[second_page] = []
    order[second_page].append(first_page)

def is_in_order(order_dict: dict[int, list[int]], nums: list[int]) -> bool:
    for i, num in enumerate(nums):
        if num in order_dict:
            for n in order_dict[num]:
                if n in nums and nums.index(n) > i:
                    return False
    
    return True

#Shoutout Harry for telling me about Kahn's algorithm
def fix_order(order_dict: dict[int, list[int]], nums: list[int]) -> list[int]:
    in_degree: dict[int, int] = {num: 0 for num in nums}
    graph: dict[int, set[int]] = {num: set() for num in nums}

    for num in nums:
        if num in order_dict:
            for dependency in order_dict[num]:
                if dependency in nums:
                    graph[dependency].add(num)
                    in_degree[num] += 1
    
    queue = deque([num for num in nums if in_degree[num] == 0])
    fixed_nums = []

    while queue:
        current = queue.popleft()
        fixed_nums.append(current)

        for dependency in graph[current]:
            in_degree[dependency] -= 1
            if in_degree[dependency] == 0:
                queue.append(dependency)

    return fixed_nums

ans = 0
ansp2 = 0
for pages in page_numbers:
    nums = [int(x) for x in pages.split(',')]
    if is_in_order(order, nums):
        ans += nums[len(nums) // 2]
    #part 2
    else:
        nums = fix_order(order, nums)
        print(nums)
        ansp2 += nums[len(nums) // 2]

print(ans)
print(ansp2)

