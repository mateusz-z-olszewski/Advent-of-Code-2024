from myutils import *
import numpy as np


class Day4(AOC):
    EXPECTED1 = 18
    EXPECTED2 = 9
    DO_BENCHMARK = True

    cardinal = [(0,1),(0,-1),(1,0),(-1,0)]
    diagonal = [(1,1),(-1,1),(1,-1),(-1,-1)]
    directions = cardinal + diagonal

    def part1(self, input : str) -> ...:
        array = np.char.array(list(map(list, input.split())))

        return sum(find_xmas(array, *dir) for dir in self.directions)

    def part2(self, input : str) -> ...:
        array = np.char.array(list(map(list, input.split())))

        diag_se = set()
        diag_sw = set()

        find_diagonal_mas(array, diag_se, 1,1)
        find_diagonal_mas(array, diag_se, -1,-1)
        find_diagonal_mas(array, diag_sw, 1,-1)
        find_diagonal_mas(array, diag_sw, -1,1)

        return len(diag_se & diag_sw)


def find_xmas(array, dx, dy):
    n = array.shape[0]
    y_range = range(max(0, -3 * dy), min(n, n + -3 * dy))
    x_range = range(max(0, -3 * dx), min(n, n + -3 * dx))
    return count_bool(is_xmas(array, y, x, dy, dx) for x in x_range for y in y_range)

def is_xmas(array, y, x, dy, dx):
    return (array[y][x] == 'X' and
            array[y + 1 * dy][x + 1 * dx] == 'M' and
            array[y + 2 * dy][x + 2 * dx] == 'A' and
            array[y + 3 * dy][x + 3 * dx] == 'S')

def find_diagonal_mas(array, results : set, dy, dx):
    n = array.shape[0]
    for y in range(1, n - 1):
        for x in range(1, n - 1):
            if array[y-dy][x-dx] == 'M' and array[y][x] == 'A' and array[y+dy][x+dx] == 'S':
                results.add((y, x))
