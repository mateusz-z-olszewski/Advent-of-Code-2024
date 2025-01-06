from math import log10
from myutils import *


class Day11(AOC):
    EXPECTED1 = 55312
    EXPECTED2 = 65601038650482 # note: not in the puzzle description, added after solving part 2

    def part1(self, input: str) -> ...:
        numbers = list(map(int, input.split()))
        return count_stones(numbers, 25)

    def part2(self, input: str) -> ...:
        numbers = list(map(int, input.split()))
        return count_stones(numbers, 75)


def count_stones(numbers: list[int], l):
    return sum(blink(k, l) for k in numbers)


@functools.cache
def blink(num, i) -> int:
    lg = int_len(num)
    digit_count_parity = lg % 2 # 1 for odd length, 0 for even
    if i == 1: return 2 - digit_count_parity
    if num == 0: return blink(1, i - 1)
    if digit_count_parity: return blink(num * 2024, i - 1)
    l, r = split_int(num, lg // 2)
    return blink(l, i - 1) + blink(r, i - 1)


@functools.cache
def int_len(x):
    return int(log10(x)+1) if x != 0 else 1


@functools.cache
def split_int(num, len):
    # split into two parts, the second one being <len> characters long
    return divmod(num, 10 ** len)
