import os
import math
import functools

dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")

with open(file_path, 'r') as reader:
    lines = [line.rstrip('\n') for line in reader]

stones = tuple(int(x) for x in lines[0].split(' '))

#before trying recursion i thought that i could get by with using a mathematical approach to finding the number of digits rather than swapping between int and str
def num_digits(n: int) -> int:
    return math.floor(math.log10(n)) + 1

@functools.lru_cache(None) # store function values for inputs we have already seen
def blink(n: int, blinks: int) -> int:
    if blinks == 0:
        count = 1
    else:
        if n == 0:
            count = blink(1, blinks - 1)
        elif num_digits(n) % 2 == 0:
            half_len = num_digits(n) // 2
            left_half = n // (10 ** half_len)
            right_half = n % (10 ** half_len)
            count = blink(left_half, blinks - 1)
            count += blink(right_half, blinks - 1)
        else:
            count = blink(2024 * n, blinks - 1)

    return count
    
#part 1
ans = sum(blink(x, 25) for x in stones)
print(ans)
#part 2
ans = sum(blink(x, 75) for x in stones)
print(ans)