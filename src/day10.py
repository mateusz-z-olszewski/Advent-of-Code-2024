from myutils import *


class Day10(AOC):
    EXPECTED1 = 36
    EXPECTED2 = 13

    def part1(self, input: str) -> ...:
        grid = parse_grid(input)
        trailheads = np.array(np.where(grid == '0')).T
        return sum(len(calculate_unique(grid, (y, x), i=0)) for y, x in trailheads)

    def part2(self, input: str) -> ...:
        grid = parse_grid(input)
        trailheads = np.array(np.where(grid == '0')).T
        return sum(calculate_repeating(grid, (y, x), i=0) for y, x in trailheads)


directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
order = list(map(str, range(0, 9)))


def calculate_unique(grid, pos, i=0):
    if not in_grid(grid, pos): return set()
    if i == 9: return {pos} if grid[pos] == '9' else set()
    if grid[pos] != order[i]: return set()
    return reduce(
        Set.union,
        (calculate_unique(grid, move(pos, dir), i=i+1) for dir in directions),
        initial=set()
    )


def calculate_repeating(grid, pos, i=0):
    if not in_grid(grid, pos): return 0
    if i == 9: return int(grid[pos] == '9')
    if grid[pos] != order[i]: return 0
    return sum(calculate_repeating(grid, move(pos, dir), i=i+1) for dir in directions)


def in_grid(grid, pos):
    return 0 <= pos[0] < grid.shape[0] and 0 <= pos[1] < grid.shape[1]


def move(current, dir):
    y, x = current
    dy, dx = dir
    return y + dy, x + dx