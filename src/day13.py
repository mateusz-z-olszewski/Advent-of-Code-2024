from myutils import *


class Day13(AOC):
    EXPECTED1 = 480
    EXPECTED2 = 875318608908 # note: not in the puzzle description, added after solving part 2

    # IMPORTANT NOTE FOR BOTH PARTS: Careful analysis of the inputs shows that no pair of
    # vectors A, B is collinear; this means to solve the problem we can simply solve the
    # system of equations, and calculate result if both coefficients are integers.

    def part1(self, input: str) -> ...:
        lines = input.split('\n')
        a_buttons = map(Button, lines[0::4])
        b_buttons = map(Button, lines[1::4])
        prizes = map(Prize, lines[2::4])
        return sum(map(solve1, a_buttons, b_buttons, prizes))


    def part2(self, input: str) -> ...:
        lines = input.split('\n')
        a_buttons = map(Button, lines[0::4])
        b_buttons = map(Button, lines[1::4])
        prizes = map(Prize, lines[2::4])
        return sum(map(solve2, a_buttons, b_buttons, prizes))


def solve1(a, b, prize) -> int:
    solved = cramer_solve(a, b, prize)
    if solved: return 3 * solved[0] + solved[1]
    return 0


def solve2(a, b, prize) -> int:
    prize.x += 10000000000000
    prize.y += 10000000000000
    solved = cramer_solve(a, b, prize)
    if solved: return 3 * solved[0] + solved[1]
    return 0


def det(a, b, c, d):
    return a * d - b * c


def cramer_solve(a, b, prize) -> tuple[int, int] | None:
    delta = det(a.dx, b.dx, a.dy, b.dy)
    d1 = det(prize.x, b.dx, prize.y, b.dy)
    d2 = det(a.dx, prize.x, a.dy, prize.y)
    p, rp = divmod(d1, delta)
    q, rq = divmod(d2, delta)
    if rp == rq == 0: return p, q
    return None


@parsing(r"Button [AB]: X\+(\d+), Y\+(\d+)")
class Button:
    dx : int
    dy : int

@parsing(r"Prize: X=(\d+), Y=(\d+)")
class Prize:
    x : int
    y : int
