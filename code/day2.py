from myutils import *


class Day2(AOC):
    EXPECTED1 = 2
    EXPECTED2 = 4

    def part1(self, input : str) -> ...:
        return chained(input,
            safe_line_split,
            map(split_row_ints),
            map(row_valid),
            count
        )

    def part2(self, input : str) -> ...:
        return chained(input,
            safe_line_split,
            map(split_row_ints),
            map(row_valid2),
            count
        )


def row_valid(row : list[int]) -> bool:
    d = list(diff(row))
    out = all(map(lambda x: -3 <= x <= -1, d)) or all(map(lambda x: 1 <= x <= 3, d))
    return out


def row_valid2(row : list[int]) -> bool:
    return row_valid(row) or any(row_valid(row[:i]+row[i+1:]) for i in range(len(row)))


def split_row_ints(row: str) -> list[int]:
    return list(map(int, row.split()))