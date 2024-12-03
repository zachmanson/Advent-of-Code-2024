import os
dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")

with open(file_path, 'r') as reader:
    string = ''.join(reader.readlines()).strip()

answer = 0

parts = string.split('mul(')
for part in parts[1:]:
    end_paren = part.find(')')
    if end_paren != -1:
        inside_mul = part[:end_paren]
        nums = inside_mul.split(',')

        if len(nums) == 2:
            first_num = nums[0].strip()
            second_num = nums[1].strip()
            if first_num.isdigit() and second_num.isdigit():
                if 1 <= len(first_num) <= 3 and 1 <= len(second_num) <= 3:
                    answer += int(first_num) * int(second_num)

print(answer)

#part 2
answer = 0
do_mult = True

parts = string.split('mul(')
for i, part in enumerate(parts):
    if i == 0:
        last_do = part.rfind('do()')
        last_dont = part.rfind("don't()")
        if last_do != -1 or last_dont != -1:
            do_mult = last_do > last_dont
        continue

    end_paren = part.find(')')
    if end_paren != -1:
        inside_mul = part[:end_paren]
        nums = inside_mul.split(',')

        if len(nums) == 2:
            first_num = nums[0].strip()
            second_num = nums[1].strip()
            if first_num.isdigit() and second_num.isdigit():
                if 1 <= len(first_num) <= 3 and 1 <= len(second_num) <= 3:
                    if do_mult:
                        answer += int(first_num) * int(second_num)

        last_do = part.rfind('do()')
        last_dont = part.rfind("don't()")
        if last_do != -1 or last_dont != -1:
            do_mult = last_do > last_dont

print(answer)
