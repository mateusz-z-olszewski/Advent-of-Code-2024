from dijkstra import Graph, DijkstraSPF

from myutils import *


N = (-1, 0)
E = (0, 1)
S = (1, 0)
W = (0, -1)
DIRS = [N, W, S, E]
ROT_L = {N: W, W: S, S: E, E: N}
ROT_R = {N: E, E: S, S: W, W: N}

class Day16(AOC):
    EXPECTED1 = 7036
    EXPECTED2 = 45

    def part1(self, input: str) -> ...:
        grid = parse_grid(input)
        _startpos = np.where(grid == 'S')
        startpos = (int(_startpos[0][0]), int(_startpos[1][0]))
        _endpos = np.where(grid == 'E')
        endpos = (int(_endpos[0][0]), int(_endpos[1][0]))

        graph = GridGraph(grid)

        posdir = (startpos, E)

        # BFS
        frontier = []
        visited = {}
        solutions = []
        paths = []

        frontier.append((*posdir, 0, (startpos,)))
        visited[posdir] = 0

        while frontier:
            selected = frontier.pop(0)
            p, d, c, path = selected
            if p == endpos:
                if not solutions or c < min(solutions):
                    solutions = [c]
                    paths = [path]
                elif c == min(solutions):
                    solutions.append(c)
                    paths.append(path)
                continue

            for pp, dd, cc in graph.neighbors((p,d), c):
                if (pp, dd) not in visited or visited[(pp, dd)] > c:
                    frontier.append((pp, dd, cc, path+(pp,)))
                    visited[(pp, dd)] = c

        # print(solutions)
        # print(*paths, sep='\n')
        return min(solutions)

    def part2(self, input: str) -> ...:
        grid = parse_grid(input)
        _startpos = np.where(grid == 'S')
        startpos = (int(_startpos[0][0]), int(_startpos[1][0]))
        _endpos = np.where(grid == 'E')
        endpos = (int(_endpos[0][0]), int(_endpos[1][0]))

        graph = Graph()
        positions = []

        # every position - direction combination is a node
        for y, x in zip(*np.where(grid != '#')):
            pos = (int(y), int(x))
            positions.append(pos)
            for dir in DIRS:
                graph.add_edge((pos, dir), (pos, ROT_L[dir]), 1000)
                graph.add_edge((pos, dir), (pos, ROT_R[dir]), 1000)
                next = addv(pos, dir)
                if inside(grid.shape, next) and grid[next] != '#':
                    graph.add_edge((pos, dir), (next, dir), 1)

        dijkstra = DijkstraSPF(graph, (startpos, E))
        path_length = distance(dijkstra, endpos)

        for p in positions:
            print(p, distance(dijkstra, p))

        # bfs from the end of all nodes which distance is 1 or 1000 smaller than its successor.
        queue = [(endpos, path_length)]
        maze = np.copy(grid)
        while queue:
            current, dist = queue.pop(0)
            maze[current] = 'O'
            for dir in DIRS:
                adj = subv(current, dir)
                if grid[adj] != '#':
                    new_dist = dijkstra.get_distance((adj, dir))
                    if dist - new_dist in {1, 1000, 1001}:
                        print('!')
                        queue.append((adj, new_dist))
        print(maze)

        return np.sum(maze == 'O')



class GridGraph:
    def __init__(self, grid):
        self.grid = grid
    def neighbors(self, posdir, cost):
        pos, dir = posdir
        current = addv(pos, dir)
        if inside(self.grid.shape, current) and self.grid[current] != '#':
            yield current, dir, cost + 1
        yield pos, ROT_L[dir], cost + 1000
        yield pos, ROT_R[dir], cost + 1000

        # c = 1
        # while inside(self.grid.shape, current) and self.grid[current] != '#':
        #     yield current, dir, cost + c
        #     current = addv(current, dir)
        #     c += 1

def distance(dijkstra, position):
    return min(dijkstra.get_distance((position, d)) for d in DIRS)


def inside(shape, p):
    return 0 <= p[0] < shape[0] and 0 <= p[1] < shape[1]