from _operator import mul
from myutils import *


class Day1(AOC):
    EXPECTED1 = 11
    EXPECTED2 = 31

    def part1(self, input: str) -> ...:
        data = input.split()
        left = sorted(map(int, data[0::2]))
        right = sorted(map(int, data[1::2]))

        return sum(map(lambda a, b: abs(a - b), left, right))

    def part2(self, input: str) -> ...:
        data = input.split()
        left = transform(data[0::2])
        right = transform(data[1::2])
        merged = merge_dicts(left, right, merger=mul)
        merged = dictmap(lambda k, v: k * v)(merged)

        return sum(merged)


def transform(input)->dict[int, int]:
    return chained(input,
        map(int),
        sorted,
        groupby_to_dict,
        dictchange(v=len)
    )
