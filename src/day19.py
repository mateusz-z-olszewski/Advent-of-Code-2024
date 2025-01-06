from myutils import *


class Day19(AOC):
    EXPECTED1 = 6
    EXPECTED2 = 16

    def parse(self, input: str):
        _patterns, _designs = input.strip().split('\n\n')
        return _patterns.split(', '), _designs.split('\n')

    def part1(self, input: str) -> ...:
        patterns, designs = self.parse(input)
        patterns.sort(key=len)
        self.pattern_groups = {k : set(v) for k, v in itertools.groupby(patterns, key=len)}
        return sum(1 for design in designs if self.matches_patterns(design))

    def part2(self, input: str) -> ...:
        patterns, designs = self.parse(input)
        patterns.sort(key=len)
        self.pattern_groups = {k: set(v) for k, v in itertools.groupby(patterns, key=len)}
        return sum(self.count_matches(design) for design in designs)

    @cache
    def matches_patterns(self, design, i=0):
        for l in self.pattern_groups.keys():
            if i + l > len(design): continue
            if i + l == len(design): return design[i:] in self.pattern_groups[l]
            if design[i:i+l] in self.pattern_groups[l] and self.matches_patterns(design, i=i+l):
                return True
        return False

    @cache
    def count_matches(self, design, i=0):
        out = 0
        for l in self.pattern_groups.keys():
            if i + l > len(design): continue
            if i + l == len(design): out += int(design[i:] in self.pattern_groups[l])
            if design[i:i+l] in self.pattern_groups[l]:
                out += self.count_matches(design, i=i+l)
        return out