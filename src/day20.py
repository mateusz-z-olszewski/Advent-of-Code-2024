from myutils import *


N = (-1, 0)
E = (0, 1)
S = (1, 0)
W = (0, -1)
directions = [N, W, S, E]


def inside(shape, p):
    return 0 <= p[0] < shape[0] and 0 <= p[1] < shape[1]



# simple because all edges are of lengths 1
def simple_dijkstra(maze, start):
    queue = deque()
    distances = np.full(maze.shape, -1, dtype=np.int32)
    queue.append((start, 0))
    distances[start] = 0
    while queue:
        pos, distance = queue.popleft()
        for d in directions:
            new = addv(pos, d)
            if not inside(maze.shape, new) or distances[new] != -1 or maze[new] == '#': continue
            queue.append((new, distance + 1))
            distances[new] = distance + 1
    return distances


def find_ends(grid):
    _startpos = np.where(grid == 'S')
    startpos = (int(_startpos[0][0]), int(_startpos[1][0]))
    _endpos = np.where(grid == 'E')
    endpos = (int(_endpos[0][0]), int(_endpos[1][0]))
    return startpos, endpos


def find_exits(grid, start, length=20) -> set[tuple[vec2, int]]:
    queue = deque()
    queue.append((start, 0))
    visited = {start}
    out = set()
    while queue:
        pos, distance = queue.popleft()
        for d in directions:
            new = addv(pos, d)
            if not inside(grid.shape, new) or new in visited: continue
            if grid[new] == '#':
                if distance < length - 1: queue.append((new, distance + 1))
            else:
                if distance < length - 1: queue.append((new, distance + 1)) # maybe extend the search using paths too?
                out.add((new, distance + 1))
            visited.add(new)
    return out


# def taxicab_iterator(grid, pos, l):
#     return filter(lambda p: grid[p] != '#', filter(partial(inside, grid.shape), (
#         (y, x)
#         for y in range(pos[0] - l, pos[0] + l)
#         for x in range(pos[1] - (l - abs(y)), pos[1] + (l - abs(y)) + 1)
#     )))


class Day20(AOC):
    EXPECTED1 = 44
    EXPECTED2 = 285


    def part1(self, input: str) -> ...:
        grid = parse_grid(input)
        threshold = 1 if grid.shape[0] <= 20 else 100
        startpos, endpos = find_ends(grid)
        start_distances = simple_dijkstra(grid, startpos)
        end_distances = simple_dijkstra(grid, endpos)
        path_length = start_distances[endpos]

        shortcut_count = 0
        for pos in np.ndindex(grid.shape):
            if grid[pos] != '#': continue
            nearby = [new for dir in directions if inside(grid.shape, new := addv(pos, dir)) and grid[new] != '#']
            if not nearby: continue
            earliest = min(start_distances[new] for new in nearby)
            latest = min(end_distances[new] for new in nearby)
            saved = path_length - earliest - latest - 2
            if saved >= threshold: shortcut_count += 1

        return shortcut_count


    def part2(self, input: str) -> ...:
        grid = parse_grid(input)
        threshold = 50 if grid.shape[0] <= 20 else 100
        startpos, endpos = find_ends(grid)
        start_distances = simple_dijkstra(grid, startpos)
        end_distances = simple_dijkstra(grid, endpos)
        path_length = start_distances[endpos]
        shortcut_count = 0
        for pos in np.ndindex(grid.shape):
            if grid[pos] == '#': continue
            for exit, l in find_exits(grid, pos):
                saved = int(path_length - start_distances[pos] - end_distances[exit] - l)
                if saved >= threshold: shortcut_count += 1
        return shortcut_count


