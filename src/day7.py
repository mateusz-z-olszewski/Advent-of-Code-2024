from myutils import *


def subtract(a, b) -> int | None:
    if a < b: return None
    return a - b


def divide(a, b) -> int | None:
    q, r = divmod(a, b)
    if r != 0: return None
    return q


def detach(a, b) -> int | None:
    sa, sb = str(a), str(b)
    if sa[-len(sb):] != sb: return None
    return int(sa[:-len(sb)])


class Day7(AOC):
    EXPECTED1 = 3749
    EXPECTED2 = 11387

    def part1(self, input : str) -> ...:
        lines = input.strip().split('\n')
        return chained(lines,
            map(Equation),
            map(Equation.solve1),
            sum
        )

    def part2(self, input : str) -> ...:
        lines = input.strip().split('\n')
        return chained(lines,
            map(Equation),
            map(Equation.solve2),
            sum
        )


@parsing(r'(\d+):(?: (\d+))+')
class Equation:
    result: int
    items: list[int]

    def solve1(self):
        if solver2(self.items, [subtract, divide], len(self.items) - 1, self.result):
            return self.result
        return 0

    def solve2(self):
        if solver2(self.items, [subtract, divide, detach], len(self.items) - 1, self.result):
            return self.result
        return 0


def solver2(items: list[int], functions, i, val) -> bool:
    if val is None: return False
    if i == -1: return val == 0
    return any(solver2(items, functions, i=i-1, val=f(val, items[i])) for f in functions)






