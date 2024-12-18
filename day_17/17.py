import os
from typing import List, Dict, Tuple, Callable, Optional

dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")

with open(file_path, 'r') as reader:
    lines = [line.rstrip('\n') for line in reader]

empty_index = lines.index('')
registers = lines[:empty_index]
program_str = lines[empty_index + 1:][0]

register = {}
register['A'] = int(registers[0].split(':')[-1])
register['B'] = int(registers[1].split(':')[-1])
register['C'] = int(registers[2].split(':')[-1])

program_str = program_str.split(':')[-1]
program = [int(x) for x in program_str.split(',')]


def get_combo_operand(register: dict[str, int], operand: int) -> int:
    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return register['A']
    elif operand == 5:
        return register['B']
    elif operand == 6:
        return register['C']
    else:
        return -1


def adv(register: dict[str, int], operand: int) -> dict[str, int]:
    divisor = 2 ** get_combo_operand(register, operand)
    if divisor != 0:
        register['A'] = register['A'] // divisor
    return register


def bxl(register: dict[str, int], operand: int) -> dict[str, int]:
    register['B'] = register['B'] ^ operand
    return register


def bst(register: dict[str, int], operand: int) -> dict[str, int]:
    register['B'] = get_combo_operand(register, operand) % 8
    return register


def jnz(register: dict[str, int], operand: int) -> tuple[bool, int]:
    if register['A'] != 0:
        return True, operand
    return False, 0


def bxc(register: dict[str, int], operand: int) -> dict[str, int]:
    register['B'] = register['B'] ^ register['C']
    return register


def out(register: dict[str, int], operand: int) -> str:
    return str(get_combo_operand(register, operand) % 8)


def bdv(register: dict[str, int], operand: int) -> dict[str, int]:
    divisor = 2 ** get_combo_operand(register, operand)
    if divisor != 0:
        register['B'] = register['A'] // divisor
    return register


def cdv(register: dict[str, int], operand: int) -> dict[str, int]:
    divisor = 2 ** get_combo_operand(register, operand)
    if divisor != 0:
        register['C'] = register['A'] // divisor
    return register

OPCODE_FUNCTIONS: dict[int, Callable[[dict[str, int], int], dict[str, int]]] = {
    0: adv,
    1: bxl,
    2: bst,
    4: bxc,
    6: bdv,
    7: cdv
}


def run(register: dict[str, int], program: list[int]) -> str:
    ip = 0
    output = []
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        
        if opcode == 3:
            jumps, ip_jump = jnz(register, operand)
            if jumps:
                ip = ip_jump
            else:
                ip += 2
        elif opcode == 5:
            output_value = out(register, operand)
            output.append(output_value)
            ip += 2
        elif opcode in OPCODE_FUNCTIONS:
            register = OPCODE_FUNCTIONS[opcode](register, operand)
            ip += 2

    return (",".join(output))

def eval_step(a: int, b: int, c: int, ip: int, program: list[int]) -> tuple[Optional[int], int, int, int, int]:
    opcode = program[ip]
    arg = program[ip + 1]
    comb = get_combo_operand({'A': a, 'B': b, 'C': c}, arg)

    if opcode == 0:
        num = a
        denom = pow(2, comb)
        return (None, num // denom, b, c, ip + 2)
    elif opcode == 1:
        return (None, a, b ^ arg, c, ip + 2)
    elif opcode == 2:
        return (None, a, comb % 8, c, ip + 2)
    elif opcode == 3:
        if a == 0:
            return (None, a, b, c, ip + 2)
        else:
            return (None, a, b, c, arg)
    elif opcode == 4:
        return (None, a, b ^ c, c, ip + 2)
    elif opcode == 5:
        return (comb % 8, a, b, c, ip + 2)
    elif opcode == 6:
        num = a
        denom = pow(2, comb)
        return (None, a, num // denom, c, ip + 2)
    elif opcode == 7:
        num = a
        denom = pow(2, comb)
        return (None, a, b, num // denom, ip + 2)

    return None

def run_program_part2(a: int, b: int, c: int, program: list[int]) -> list[int]:
    ip = 0
    res = []
    while ip < len(program) - 1:
        out, a, b, c, ip = eval_step(a, b, c, ip, program)
        if out is not None:
            res.append(out)
    return res


def get_best_quine_input(program: list[int], cursor: int, sofar: int) -> Optional[int]:
    for candidate in range(8):
        if run_program_part2(sofar * 8 + candidate, 0, 0, program) == program[cursor:]:
            if cursor == 0:
                return sofar * 8 + candidate
            ret = get_best_quine_input(program, cursor - 1, sofar * 8 + candidate)
            if ret is not None:
                return ret
    return None


print(run(register, program))
print(get_best_quine_input(program, len(program) - 1, 0))