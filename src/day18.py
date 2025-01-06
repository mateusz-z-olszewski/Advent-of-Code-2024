from myutils import *
from collections import deque


N = (-1, 0)
E = (0, 1)
S = (1, 0)
W = (0, -1)
directions = [N, W, S, E]


def inside(shape, p):
    return 0 <= p[0] < shape[0] and 0 <= p[1] < shape[1]


def search_bfs(maze, start, end):
    queue = deque()
    visited = np.zeros(maze.shape)
    queue.append((start, [start]))
    visited[start] = 1
    while queue:
        pos, path = queue.popleft()
        if pos == end: return path
        for d in directions:
            new = addv(pos, d)
            if not inside(maze.shape, new) or visited[new] or maze[new] == 1: continue
            queue.append((new, path + [new]))
            visited[new] = 1
    return -1


def validate_bfs(maze, start, end):
    queue = deque()
    visited = np.zeros(maze.shape)
    queue.append(start)
    visited[start] = 1
    while queue:
        pos = queue.popleft()
        if pos == end: return True
        for d in directions:
            new = addv(pos, d)
            if not inside(maze.shape, new) or visited[new] or maze[new] == 1: continue
            queue.append(new)
            visited[new] = 1
    return False


def print_grid(grid):
    for row in grid:
        for item in row:
            dict = {0: '.', 1: '#', 2: 'O', 3: 'X'}
            print(dict[item], flush=False, end='')
        print()


class Day18(AOC):
    EXPECTED1 = 22
    EXPECTED2 = (6, 1)

    def part1(self, input: str) -> ...:
        if len(input) < 100: shape, count = (7, 7), 12
        else: shape, count = (71, 71), 1024
        grid = np.zeros(shape, dtype=np.int8)
        for i, line in zip(range(count), input.split('\n')):
            _x, _y = line.split(',')
            y, x = int(_y), int(_x)
            grid[y, x] = 1
        end = addv(shape, (-1, -1))
        path = search_bfs(grid, (0,0), end)
        # for p in path: grid[p] = 2
        return len(path) - 1


    def part2(self, input: str) -> ...:
        if len(input) < 100: shape, count = (7, 7), 12
        else: shape, count = (71, 71), 1024
        grid = np.zeros(shape, dtype=np.int8)
        for i, line in zip(range(count), input.split('\n')):
            _x, _y = line.split(',')
            y, x = int(_y), int(_x)
            grid[y, x] = 1
        end = addv(shape, (-1, -1))
        out = ()
        for _i, line in enumerate(input.strip().split('\n')[count:]):
            _x, _y = line.split(',')
            pos = int(_y), int(_x)
            grid[pos] = 1
            i = _i + count
            if not validate_bfs(grid, (0,0), end):
                out = pos
                print(i)
                grid[pos] = 0
                path = search_bfs(grid, (0, 0), end)
                for p in path: grid[p] = 2
                grid[pos] = 3
                print_grid(grid)
                break

        return out[1], out[0]


