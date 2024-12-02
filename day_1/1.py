import os
dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")

with open(file_path, 'r') as reader:
    lines = [line.rstrip('\n') for line in reader]

left_list = [int(line.split()[0]) for line in lines]
right_list = [int(line.split()[1]) for line in lines]

sorted_left = sorted(left_list)
sorted_right = sorted(right_list)

distances = [abs(left - right) for left, right in zip(sorted_left, sorted_right)]
print(sum(distances))

#part 2
similarity_score = 0
for n in left_list:
    similarity_score += n * right_list.count(n)
print(similarity_score)