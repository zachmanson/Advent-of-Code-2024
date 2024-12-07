import os
dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")
from itertools import product

with open(file_path, 'r') as reader:
    lines = [line.rstrip('\n') for line in reader]

operations = ['+', '*']

ans = 0
for line in lines:
    target_str, nums_str = line.split(':')
    target = int(target_str)
    nums = [int(x) for x in nums_str.split(' ')[1:]]

    num_operations = len(nums) - 1
    #loop thru cartesian product of operations list with itself num_operations times:
    for ops in product(operations, repeat = num_operations):
        total = nums[0]
        for i, op in enumerate(ops):
            if op == '+':
                total += nums[i + 1]
            else:
                total *= nums[i + 1]

        if total == target:
            ans += target
            break

print(ans)

#part 2
operations = ['+', '*', '||']
ans = 0
for line in lines:
    target_str, nums_str = line.split(':')
    target = int(target_str)
    nums = [int(x) for x in nums_str.split(' ')[1:]]

    num_operations = len(nums) - 1
    for ops in product(operations, repeat = num_operations):
        total = nums[0]
        for i, op in enumerate(ops):
            if op == '+':
                total += nums[i + 1]
            elif op == '*':
                total *= nums[i + 1]
            else:
                total = int(str(total) + str(nums[i+1]))

        if total == target:
            ans += target
            break

print(ans)