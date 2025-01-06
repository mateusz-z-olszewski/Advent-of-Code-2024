from myutils import *
from unionfind import unionfind


class Day12(AOC):
    EXPECTED1 = 140
    EXPECTED2 = 80

    def part1(self, input: str) -> ...:
        grid = parse_grid(input)
        print(list(array_valid_positions(grid, S)))


        size = grid.shape[0] * grid.shape[1]
        uf = unionfind(size)
        fences = np.zeros(grid.shape, dtype=np.int64)

        for pos in array_valid_positions(grid, S):
            evaluate(pos, addv(pos, S), grid, fences, uf)
        for pos in array_valid_positions(grid, E):
            evaluate(pos, addv(pos, E), grid, fences, uf)
        add_borders(fences)

        total = 0
        for group in uf.groups():
            total_fences = 0
            for pos_no in group:
                pos = unconvert(pos_no, grid)
                total_fences += fences[pos]
            total += len(group) * total_fences


        return int(total)

    def part2(self, input: str) -> ...:
        grid = parse_grid(input)
        size = grid.shape[0] * grid.shape[1]
        uf = unionfind(size)

        # create regions
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1] - 1):
                evaluate((y, x), (y, x + 1), grid, None, uf)
        for x in range(grid.shape[1]):
            for y in range(grid.shape[0] - 1):
                evaluate((y, x), (y + 1, x), grid, None, uf)

        # add single fences
        right_sides = np.full(grid.shape, -1, dtype=np.int32)
        left_sides = np.full(grid.shape, -1, dtype=np.int32)
        down_sides = np.full(grid.shape, -1, dtype=np.int32)
        up_sides = np.full(grid.shape, -1, dtype=np.int32)
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                add_side((y, x), (y, x - 1), grid, left_sides, uf)
                add_side((y, x), (y, x + 1), grid, right_sides, uf)
        for x in range(grid.shape[1]):
            for y in range(grid.shape[0]):
                add_side((y, x), (y - 1, x), grid, up_sides, uf)
                add_side((y, x), (y + 1, x), grid, down_sides, uf)

        sizes = make_size_grid(uf.groups(), grid)


        return sum([
            calc_h(up_sides, sizes),
            calc_h(down_sides, sizes),
            calc_h(left_sides.T, sizes.T),
            calc_h(right_sides.T, sizes.T)
        ]) # 4 + 4 + 4 + 1 + 4 + 3 = 20



def convert(y, x, grid):
    return y * grid.shape[0] + x
def unconvert(pos_no, grid):
    return divmod(pos_no, grid.shape[0])


def evaluate(pos, next, grid, fences, uf):
    if grid[pos] == grid[next]:
        uf.unite(convert(*pos, grid), convert(*next, grid))
    elif fences is not None:
        fences[pos] += 1
        fences[next] += 1

def add_side(pos, next, grid, sides, uf):
    if inside(grid.shape, next):
        if grid[pos] != grid[next]:
            sides[pos] = uf.find(convert(*pos, grid))
    else: sides[pos] = uf.find(convert(*pos, grid))

def calc_h(sides, sizes):
    total = 0
    for y in range(sides.shape[0]):
        width = sides.shape[1]
        x = 0
        while x < width:
            while x < width and sides[y, x] == -1: x += 1
            if x == width: break
            total += sizes[y, x]
            last = sides[y, x]
            while x < width and sides[y, x] == last: x += 1
    return total


def add_borders(fences):
    h, w = fences.shape
    for y in range(h):
        fences[y, 0] += 1
        fences[y, w - 1] += 1
    for x in range(w):
        fences[0, x] += 1
        fences[h - 1, x] += 1


def inside(shape, p):
    return 0 <= p[0] < shape[0] and 0 <= p[1] < shape[1]


def make_size_grid(groups : list[list[int]], grid):
    out = np.zeros(grid.shape, dtype=np.int32)
    for group in groups:
        l = len(group)
        for item in group:
            out[unconvert(item, grid)] = l
    return out
