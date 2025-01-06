from myutils import *

def inside(shape, p):
    return 0 <= p[0] < shape[0] and 0 <= p[1] < shape[1]


class Day8(AOC):
    EXPECTED1 = 14
    EXPECTED2 = 34

    def part1(self, input : str) -> ...:
        grid = parse_grid(input)
        groups = groupby_array(grid)
        out = chained(groups.values(),
            map(antinodes1),
            reduce(Set.union, initial=set()),
            filter(partial(inside, grid.shape)),
            iterable_len
        )
        return out

    def part2(self, input: str) -> ...:
        grid = parse_grid(input)
        groups = groupby_array(grid)
        out = chained(groups.values(),
            map(lambda g : antinodes2(g, grid.shape)),
            reduce(Set.union, initial=set()),
            filter(partial(inside, grid.shape)),
            iterable_len
        )
        return out


def antinodes1(group):
    out = set()
    for l, r in itertools.combinations(group, 2):
        d = subv(l, r)
        out.add(addv(l, d))
        out.add(subv(r, d))
    return out


def antinodes2(group, shape):
    out = set()
    for l, r in itertools.combinations(group, 2):
        d = subv(l, r)
        result = l
        while inside(shape, result):
            out.add(result)
            result = addv(result, d)
        result = r
        while inside(shape, result):
            out.add(result)
            result = subv(result, d)
    return out


def addv(current, dir):
    y, x = current
    dy, dx = dir
    return y + dy, x + dx


def subv(current, dir):
    y, x = current
    dy, dx = dir
    return y - dy, x - dx


def groupby_array(array: np.ndarray) -> dict:
    out = {}
    for pos, val in np.ndenumerate(array):
        if val == '.': continue
        if val in out: out[val].append(pos)
        else: out[val] = [pos]
    return out