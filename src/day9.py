from myutils import *
import operator
from dataclasses import dataclass


@dataclass
class Block:
    start : int
    length : int
    id : int

@dataclass
class Span:
    start : int
    length : int


class Day9(AOC):
    EXPECTED1 = 1928
    EXPECTED2 = 2858

    def part1(self, input : str) -> ...:
        input = list(map(int, input.strip()))
        files = input[0::2]
        spaces = input[1::2]

        disk_mapping = []
        di = 0
        for f, s in zip(files, spaces + [0]):
            disk_mapping.extend([di] * f)
            di += 1
            disk_mapping.extend([None] * s)

        reorder(disk_mapping)
        return sum(map(operator.mul, range(len(disk_mapping)), disk_mapping))


    def part2(self, input: str) -> ...:
        input = list(map(int, input.strip()))

        filled: list[Block] = []
        empty: list[Span] = []
        i = 0
        for j, v in enumerate(input):
            val = int(v)
            if j % 2 == 0:
                filled.append(Block(i, val, j // 2))
            elif val != 0:
                empty.append(Span(i, val))
            i += int(v)

        # changes block/span starts and lengths in place
        for block in reversed(filled):
            for span in empty:
                if span.start > block.start: break  # no need to search further
                if span.length < block.length: continue
                block.start = span.start
                span.start += block.length
                span.length -= block.length

        return sum(map(calc, filled))

    def part2new(self, input : str) -> ...:
        input = list(map(int, input.strip()))

        blocks : list[Block] = []
        spans : GroupingPriorityQueue[Span] = GroupingPriorityQueue(lambda s: s.length, lambda s: s.start)
        i = 0
        for j, v in enumerate(input):
            val = int(v)
            if j % 2 == 0: blocks.append(Block(i, val, j // 2))
            elif val != 0: spans.insert(Span(i, val))
            i += int(v)

        print(blocks)
        # changes block/span starts and lengths in place
        for block in reversed(blocks):
            found = False
            for l in range(block.length, 10):
                span = spans.replace(l, replacer(block))
                if span is not None:
                    found = True
                    #print(block, span)
                    break
            if not found: print("Did not move ", block)


        return sum(map(calc, blocks))


def replacer(block):
    def _inner(span):
        if span is None: return None
        if span.start > block.start: return None
        print(block, span, end=" | ")
        block.start = span.start
        span.start += block.length
        span.length -= block.length
        print(block, span)
        return span
    return _inner


def reorder(disk_mapping: list[int|None]):
    for i in range(sum(1 for d in disk_mapping if d is not None)):
        if disk_mapping[i] is not None:
            continue
        while disk_mapping[-1] is None: disk_mapping.pop()
        disk_mapping[i] = disk_mapping.pop()
    while disk_mapping[-1] is None: disk_mapping.pop()


def calc(input : Block):
    return input.id * sum(range(input.start, input.start + input.length))