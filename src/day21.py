from myutils import *

numeric_columns = {
    '7':0, '8':1, '9':2,
    '4':0, '5':1, '6':2,
    '1':0, '2':1, '3':2,
           '0':1, 'A':2
}
numeric_rows = {
    '7':0, '8':0, '9':0,
    '4':1, '5':1, '6':1,
    '1':2, '2':2, '3':2,
           '0':3, 'A':3
}
directional_columns = {
           '^':1, 'A':2,
    '<':0, 'v':1, '>':2
}
directional_rows = {
           '^':0, 'A':0,
    '<':1, 'v':1, '>':1
}
arrows = {
    '^' : (-1, 0),
    '>' : (0, 1),
    'v' : (1, 0),
    '<' : (0, -1)
}
numeric = parse_grid("789\n456\n123\n.0A")
directional = parse_grid(".^A\n<v>")


def debug(input, grid):
    pos = (3, 2) if grid is numeric else (0, 2)
    out = ''
    for i in input:
        if i == 'A': out += grid[pos]
        else: pos = addv(pos, arrows[i])
    return out

def hdir(x):
    if x == 0: return ''
    if x > 0: return '>' * x
    else: return '<' * -x


def vdir(x):
    if x == 0: return ''
    if x > 0: return 'v' * x
    else: return '^' * -x



class Day21(AOC):
    EXPECTED1 = 126384
    EXPECTED2 = 154115708116294 # note: not in the puzzle description, added after solving part 2

    def parse(self, input: str):
        return [line for line in input.strip().split('\n')]

    def part1(self, input: str) -> ...:
        lines = self.parse(input)
        return sum(int(line[:-1]) * complexity_numeric(line) for line in lines)

    def part2(self, input: str) -> ...:
        lines = self.parse(input)
        return sum(int(line[:-1]) * complexity_numeric(line, k=25+1) for line in lines)



def complexity_numeric(input: str, k=3) -> int:
    out = 0
    last = 'A'
    for t in input:
        out += path_length_numeric(last, t, k)
        last = t
    return out


def path_length_numeric(f, t, k):
    fy, fx = numeric_rows[f], numeric_columns[f]
    ty, tx = numeric_rows[t], numeric_columns[t]
    h_first: bool
    if min(fx, tx) == 0 and max(fy, ty) == 3:
        # case when there is only one path, as the other one would pass through the empty corner.
        h_first = fx < tx
        hd, vd = hdir(tx - fx), vdir(ty - fy)
        path = hd + vd + 'A' if h_first else vd + hd + 'A'
        return complexity_directional(path, k - 1)
    return min(
        complexity_directional(hdir(tx - fx) + vdir(ty - fy) + 'A', k - 1),
        complexity_directional(vdir(ty - fy) + hdir(tx - fx) + 'A', k - 1),
    )


dirpaths = {
    'AA': ['A'], 'A>': ['vA'], 'A^': ['<A'], 'Av': ['v<A', '<vA'], 'A<': ['v<<A'],
    '>A': ['^A'], '>>': ['A'], '>^': ['<^A', '^<A'], '>v': ['<A'], '><': ['<<A'],
    '^A': ['>A'], '^>': ['v>A', '>vA'], '^^': ['A'], '^v': ['vA'], '^<': ['v<A'],
    'vA': ['>^A', '^>A'], 'v>': ['>A'], 'v^': ['^A'], 'vv': ['A'], 'v<': ['<A'],
    '<A': ['>>^A'], '<>': ['>>A'], '<^': ['>^A'], '<v': ['>A'], '<<': ['A'],
}


@cache
def complexity_directional(path, k) -> int:
    if k == 0: return len(path)
    out = 0
    last = 'A'
    for t in path:
        jump = last + t
        out += min(complexity_directional(new_path, k - 1) for new_path in dirpaths[jump])
        last = t
    return out