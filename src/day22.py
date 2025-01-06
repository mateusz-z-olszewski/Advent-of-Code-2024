from myutils import *


class Day22(AOC):
    EXPECTED1 = 37327623
    EXPECTED2 = 23

    MOD = 16777216

    def __init__(self, *args):
        super().__init__(*args)

        array = np.arange(self.MOD, dtype=np.int32)
        array = (array << 6 ^ array) % self.MOD
        array = (array >> 5 ^ array) % self.MOD
        self.hash = (array << 11 ^ array) % self.MOD

    def parse(self, input: str):
        return [int(line) for line in input.strip().split('\n')]

    def part1(self, input: str) -> ...:
        lines = self.parse(input)
        return sum(self.monkey_hash(num) for num in lines)

    def part2(self, input: str) -> ...:
        lines = self.parse(input)
        l = len(lines)

        values, differences = [], []
        for num in lines:
            vals, diffs = self.generate_arrays(num)
            values.append(vals)
            differences.append(diffs)

        sequence_values = np.zeros((l, 19, 19, 19, 19), dtype=np.int32)
        print("Array size (bytes):", sequence_values.nbytes)
        for i, diffs in enumerate(differences):
            layer = sequence_values[i]
            vals = values[i]
            # reversed because we select the first one, and it is cheaper to iterate few times more
            # than keep track of seen combinations and having conditional statements.
            for j in reversed(range(3, len(diffs))):
                seq = tuple(diffs[j-3:j+1])
                layer[seq] = vals[j]

        totals = np.sum(sequence_values, axis=0)
        return int(np.max(totals))


    def monkey_hash(self, num, n=2000):
        for _ in range(n):
            num = self.hash[num]
        return int(num)


    def generate_arrays(self, number, n=2000):
        vals, diffs = np.zeros((n-1,), dtype=np.int8), np.zeros((n-1,), dtype=np.int8)
        num = number
        for i in range(n-1):
            num = self.hash[num]
            vals[i] = num % 10
        diffs[1:] = vals[1:] - vals[:-1]
        diffs[0] = vals[0] - (number % 10)
        return vals, diffs