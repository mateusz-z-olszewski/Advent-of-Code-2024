from myutils import *


def print_grid(grid):
    for row in grid:
        for item in row:
            print(item, flush=False, end='')
        print()


N = (-1, 0)
E = (0, 1)
S = (1, 0)
W = (0, -1)
DIRS = {
    '^': N,
    '<': W,
    'v': S,
    '>': E
}

class Day15(AOC):
    EXPECTED1 = 2028
    EXPECTED2 = 9021

    def part1(self, input: str) -> ...:
        grid = parse_grid(input.split('\n\n')[0])
        directions = input.split('\n\n')[1].replace('\n', '')

        _startpos = np.where(grid == '@')
        pos = (_startpos[0][0], _startpos[1][0])

        # move(grid)
        for dir in directions:
            moved = move(grid, pos, DIRS[dir])
            if moved: pos = addv(pos, DIRS[dir])
        return sum_gps(grid)

    def part2(self, input: str) -> ...:
        narrow_grid = parse_grid(input.split('\n\n')[0])
        directions = input.split('\n\n')[1].replace('\n', '')

        _startpos = np.where(narrow_grid == '@')
        pos = (_startpos[0][0], 2 * _startpos[1][0])

        height, prev_width = narrow_grid.shape
        grid = np.zeros((height, prev_width * 2), dtype=np.str_)
        grid[:, 0::2] = narrow_grid
        grid[:, 1::2] = narrow_grid
        grid[addv(pos, E)] = '.'
        make_boxes(grid)
        print_grid(grid)

        for i, dir in enumerate(directions):
            print(i, dir)
            pass
            if dir in "<>":
                moved = move(grid, pos, DIRS[dir])
                if moved: pos = addv(pos, DIRS[dir])
            else:
                f = move_wait(grid, pos, DIRS[dir])
                if f is not None:
                    f()
                    pos = addv(pos, DIRS[dir])
            validate(grid)
            # print_grid(grid)
            # builtins.input()

        print_grid(grid)
        return sum_gps(grid)

def move(grid, pos, dir):
    if grid[pos] == '#': return False
    new = addv(pos, dir)
    if grid[new] == '.':
        grid[new] = grid[pos]
        grid[pos] = '.'
        return True
    if move(grid, new, dir):
        grid[new] = grid[pos]
        grid[pos] = '.'
        return True
    return False


def move_wait(grid, pos, dir):
    if grid[pos] == '#': return None
    if grid[pos] == '.': return lambda: None
    new = addv(pos, dir)
    # print(pos, new, match_box(grid, new))

    if grid[pos] == '@': # moving a robot
        if grid[new] == '.': # onto a free space
            def _inner():
                grid[new] = grid[pos]
                grid[pos] = '.'
            return _inner
        elif grid[new] == '#': # onto a wall
            return None
        else: # pushing some boxes
            next = move_wait(grid, new, dir)
            if next is not None:
                def _inner():
                    next()
                    grid[new] = grid[pos]
                    grid[pos] = '.'
                return _inner
            else:
                return None

    # moving a box
    nearby = match_box(grid, pos)
    nearby_new = addv(nearby, dir)

    # next pushed box is aligned
    if match_box(grid, new) == nearby_new:
        f = move_wait(grid, new, dir)
        if f is not None: # next pushed box can actually be pushed
            def _inner():
                f()
                grid[new] = grid[pos]
                grid[nearby_new] = grid[nearby]
                grid[pos] = '.'
                grid[nearby] = '.'
            return _inner
        return None # next box is blocked


    a, b = move_wait(grid, new, dir), move_wait(grid, nearby_new, dir)
    # next_a_empty, next_b_empty = grid[new] == '.', grid[nearby_new] == '.'
    # if (a is not None or next_a_empty) and (b is not None and next_b_empty):
    if a is not None and b is not None:
        BOX = {'[', ']'}
        # can move the whole box
        def _inner():
            # print(grid[new], grid[match_box(grid, new)])
            if a and match_box(grid, new) and {grid[new], grid[match_box(grid, new)]} == BOX: a()
            if b and match_box(grid, nearby_new) and {grid[nearby_new], grid[match_box(grid, nearby_new)]} == BOX: b()
            if {grid[pos], grid[nearby]} == BOX:
                grid[new] = grid[pos]
                grid[nearby_new] = grid[nearby]
                grid[pos] = '.'
                grid[nearby] = '.'
        return _inner
    return None


def sum_gps(grid):
    total = 0
    for pos in np.ndindex(grid.shape):
        if grid[pos] == 'O' or grid[pos] == '[':
            total += 100 * pos[0] + pos[1]
    return total


def make_boxes(grid):
    for row in grid:
        open = True
        for x in range(grid.shape[1]):
            if row[x] == 'O':
                row[x] = '[' if open else ']'
                open ^= True


def match_box(grid, pos):
    if grid[pos] == '[': return addv(pos, E)
    elif grid[pos] == ']': return addv(pos, W)
    else: return None


def validate(grid):
    for row in grid:
        for x in range(grid.shape[1]):
            if row[x] == '[' and row[x + 1] != ']':
                print("!")

