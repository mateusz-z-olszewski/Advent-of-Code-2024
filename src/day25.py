from myutils import *


class Day25(AOC):
    EXPECTED1 = 3

    def parse(self, input):
        grids = input.strip().split('\n\n')
        locks, keys = [], []
        for g in grids:
            grid = parse_grid(g)
            heights = np.sum(grid == '#', axis=0) - 1
            if grid[0,0] == '#': locks.append(heights)
            else: keys.append(heights)
        return locks, keys




    def part1(self, input: str) -> ...:
        locks, keys = self.parse(input)

        out = 0
        for l, k in itertools.product(locks, keys):
            fits = np.all(l + k <= 5)
            if fits: out += 1
        return out

    def part2(self, input: str) -> ...:
        return ...