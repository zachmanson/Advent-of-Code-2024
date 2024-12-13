import os
import re

A_COST = 3
B_COST = 1

dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")

with open(file_path, 'r') as reader:
    lines = [line.rstrip('\n') for line in reader]

tokens = 0
tokens_p2 = 0
for i in range(0, len(lines), 4):
    machine_info = lines[i:i+3]
    current_machine = {}
    
    A_info = re.match(r'Button A: X([+-]\d+), Y([+-]\d+)', machine_info[0])
    current_machine['A'] = (int(A_info.group(1)), int(A_info.group(2)))
    
    B_info = re.match(r'Button B: X([+-]\d+), Y([+-]\d+)', machine_info[1])
    current_machine['B'] = (int(B_info.group(1)), int(B_info.group(2)))

    prize_info = re.match(r'Prize: X=(\d+), Y=(\d+)', machine_info[2])
    current_machine['Prize'] = (int(prize_info.group(1)), int(prize_info.group(2)))

    #solving
    # a A_presses + b B_presses = p
    # c A_presses + d B_presses = q
    # solve this using lin alg by hand

    a = current_machine['A'][0]
    b = current_machine['B'][0]
    c = current_machine['A'][1]
    d = current_machine['B'][1]
    p = current_machine['Prize'][0]
    q = current_machine['Prize'][1]

    det = a * d - b * c
    if det != 0:
        A_presses = (d * p - b * q) / (a * d - b * c)
        B_presses = (- c * p + a * q) / (a * d - b * c)

        if A_presses.is_integer() and B_presses.is_integer() and 0 < A_presses <= 100 and 0 < B_presses <= 100:
            tokens += int((A_presses * A_COST) + (B_presses * B_COST))

    #gonna keep part 2 separate 
    p = current_machine['Prize'][0] + 10000000000000
    q = current_machine['Prize'][1] + 10000000000000
    if det != 0:
        A_presses = (d * p - b * q) / (a * d - b * c)
        B_presses = (- c * p + a * q) / (a * d - b * c)

        if A_presses.is_integer() and B_presses.is_integer():
            tokens_p2 += int((A_presses * A_COST) + (B_presses * B_COST))

print(tokens)
print(tokens_p2)

            


