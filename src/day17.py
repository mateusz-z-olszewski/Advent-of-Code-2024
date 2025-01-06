from myutils import *


class Day17(AOC):
    EXPECTED1 = [4,6,3,5,6,3,5,2,1,0]
    EXPECTED2 = ... # no expected value for p1 as it uses a different program

    def part1(self, input: str) -> ...:
        a, b, c, *instructions = map(int, regex.findall(r'\d+', input))
        cpu = CPU(a, b, c)
        return cpu.execute(instructions)

    def part2(self, input: str) -> ...:
        _, _, _, *instructions = map(int, regex.findall(r'\d+', input))
        if len(instructions) == 6: return ...
        # my solution only works with my own input.
        self.assertEqual(instructions, [2,4,1,1,7,5,4,0,0,3,1,6,5,5,3,0])
        return min(part2(instructions))


def part2(expected):
    """
    Calculates a list of all numbers which lead to the given sequence when run on the full input problem.
    """
    rev = list(reversed(expected))
    queue = [(0, 0)]
    out = []
    while queue:
        a, i = queue.pop(0)
        if i == len(expected):
            out.append(a)
            continue
        start = 0 if i else 1 # start from 1 on first iteration.
        b = rev[i]
        for x in range(start, 8):
            new_a = (a << 3) + x
            if 7 ^ x ^ ((new_a >> (x ^ 1)) % 8) == b:
                queue.append((new_a, i + 1))
    return out


def simplified(a):
    """
    Behaves exactly like the whole CPU assuming that a=a, b=c=0, instructions are as in my puzzle input:

    START:
    |   MOD A, 8 -> B
    |   XOR B, 1 -> B
    |   SHR A, B -> C
    |   XOR B, C -> B
    |   SHR A, 3 -> A
    |   XOR B, 6 -> 6
    |   OUT (B % 8)
    |   JNZ START

    That is why my solution only works for this input.
    """
    out = []
    while a:
        m = a % 8
        cc = (a >> (m ^ 1)) % 8
        out.append(7 ^ m ^ cc)
        a //= 8
    return out


class CPU:
    out: list[int]

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.ip = 0

        self.OPCODES = [self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv]

    def execute(self, program: list[int]) -> list[int]:
        self.out = []
        while self.ip < len(program):
            instr = self.OPCODES[program[self.ip]]
            operand = program[self.ip + 1]
            self.ip += 2
            instr(operand)
        return self.out

    def adv(self, op):
        self.a >>= self.combo(op)

    def bxl(self, op):
        self.b ^= op

    def bst(self, op):
        self.b = (self.combo(op) % 8)

    def jnz(self, op):
        if self.a == 0: return
        self.ip = op

    def bxc(self, _):
        self.b ^= self.c

    def out(self, op):
        self.out.append(self.combo(op) % 8)

    def bdv(self, op):
        self.b = self.a >> self.combo(op)

    def cdv(self, op):
        self.c = self.a >> self.combo(op)

    def combo(self, op):
        if op <= 3: return op
        if op == 4: return self.a
        if op == 5: return self.b
        if op == 6: return self.c
        raise Exception("Combo operation with argument 7")