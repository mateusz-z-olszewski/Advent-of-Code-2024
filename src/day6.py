from ast import parse

import numpy as np

from myutils import *


class Day6(AOC):
    EXPECTED1 = 41
    EXPECTED2 = 6

    N = (-1, 0)
    E = (0, 1)
    S = (1, 0)
    W = (0, -1)
    rot = {N: E, E: S, S: W, W: N}

    def part1(self, input: str) -> ...:
        grid = parse_grid(input)
        _startpos = np.where(grid == '^')
        startpos = (_startpos[0][0], _startpos[1][0])
        visited = self.find_visited(grid, startpos)
        return np.sum(visited)

    def part2(self, input: str) -> ...:
        grid = parse_grid(input)
        _startpos = np.where(grid == '^')
        startpos = (_startpos[0][0], _startpos[1][0])
        out = 0
        itno = 0
        visited = self.find_visited(grid, startpos)
        for pos, val in np.ndenumerate(grid):
                if grid[pos] == '.' and visited[pos] == 1:
                    grid[pos] = '#'
                    if self.find_loop(grid, startpos): out += 1
                    grid[pos] = '.'
                itno += 1
                if itno % 100 == 0: print(itno)
        return out

    def find_visited(self, grid, startpos):
        dir = self.N
        visited = np.zeros(shape=grid.shape, dtype=np.uint8)
        visited[startpos] = 1
        current = startpos
        while in_grid(grid, move(current, dir)):
            new = move(current, dir)
            if grid[new] == '#':
                dir = self.rot[dir]
            else:
                current = new
                visited[new] = 1

        return visited

    def find_loop(self, grid, startpos):
        dir = self.N
        visited = np.zeros(shape=(4,)+grid.shape, dtype=np.uint8)
        visited[self.pos_dir(startpos, dir)] = 1
        current = startpos
        while in_grid(grid, move(current, dir)):
            new = move(current, dir)
            if grid[new] == '#':
                dir = self.rot[dir]
            else:
                current = new
                pd = self.pos_dir(current, dir)
                if visited[pd] == 1:
                    return True
                visited[pd] = 1
        return False

    def pos_dir(self, pos, dir):
        if dir == self.N: return 0, *pos
        if dir == self.E: return 1, *pos
        if dir == self.S: return 2, *pos
        if dir == self.W: return 3, *pos


def in_grid(grid, pos):
    return 0 <= pos[0] < grid.shape[0] and 0 <= pos[1] < grid.shape[1]


def move(current, dir):
    y, x = current
    dy, dx = dir
    return y + dy, x + dx



