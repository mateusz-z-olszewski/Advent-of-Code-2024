from myutils import *


np.set_printoptions(threshold=105)

def safety_factor(robots, height, width):
    half_y = height // 2
    half_x = width // 2

    ne, nw, sw, se = 0,0,0,0
    for robot in robots:
        if robot.px > half_x:
            if robot.py > half_y: se += 1
            elif robot.py < half_y: ne += 1
        elif robot.px < half_x:
            if robot.py > half_y: sw += 1
            elif robot.py < half_y: nw += 1
    return ne * nw * sw * se


def print_grid(grid):
    for row in grid:
        for item in row:
            print('#' if item == 1 else ' ', flush=False, end='')
        print()


class Day14(AOC):
    EXPECTED1 = 12
    def part1(self, input: str) -> ...:
        robots = list(map(Robot, input.strip().split('\n')))
        if len(robots) > 20: width, height = 101, 103
        else: width, height = 11, 7

        for robot in robots:
            robot.move(100, height, width)
        return safety_factor(robots, height, width)

    def part2(self, input: str) -> ...:
        START = 70
        STEP = 1


        input = open(r"C:\Users\Mateusz\PycharmProjects\Advent Of Code 2024\inputs\day14\full.txt", 'r').read()
        robots = list(map(Robot, input.strip().split('\n')))
        if len(robots) > 20:
            width, height = 101, 103
        else:
            width, height = 11, 7

        for robot in robots:
            robot.move(START, height, width)

        for i in range(START, 10000,  STEP):
            grid = np.zeros((height, width))


            for robot in robots:
                grid[robot.py, robot.px] = 1
                robot.move(STEP, height, width)
            print_grid(grid)
            print("^^^^^^", i)
            builtins.input()


@parsing(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")
class Robot:
    px : int
    py : int
    vx : int
    vy : int

    def move(self, n, height, width):
        self.px = (self.px + self.vx * n) % width
        self.py = (self.py + self.vy * n) % height

