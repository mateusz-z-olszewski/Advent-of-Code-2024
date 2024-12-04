from myutils import *
import re


class Day3(AOC):
    EXPECTED1 = 161
    EXPECTED2 = 48

    enabled : bool

    def part1(self, input : str) -> ...:
        pattern = re.compile(r'mul\((\d+),(\d+)\)')
        out = chained(pattern.finditer(input),
            map(self.mul_match),
            sum
        )
        return out

    def part2(self, input):
        pattern = re.compile(r"do\(\)|don't\(\)|mul\((\d+),(\d+)\)")
        self.enabled = True
        out = chained(pattern.finditer(input),
            map(self.handle),
            sum
        )
        return out

    def mul_match(self, p):
        return int(p.group(1)) * int(p.group(2))

    def handle(self, p):
        if p.group(0) == 'do()':
            self.enabled = True
            return 0
        elif p.group(0) == 'don\'t()':
            self.enabled = False
            return 0
        else:
            return self.mul_match(p) * int(self.enabled)
