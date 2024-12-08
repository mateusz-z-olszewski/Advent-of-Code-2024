import graphlib

from myutils import *


class Day5(AOC):
    EXPECTED1 = 143
    EXPECTED2 = 123

    def part1(self, input : str) -> ...:
        _rules, _updates = input.strip().split('\n\n')
        rules = split_multiple(_rules, '\n', '|', atom_f=int)
        out = chained(split_multiple(_updates, '\n', ',', atom_f=int),
            filter(lambda l: in_dag(l, rules)),
            map(median),
            sum
        )
        return out

    def part2(self, input : str) -> ...:
        _rules, _updates = input.strip().split('\n\n')
        rules = split_multiple(_rules, '\n', '|', atom_f=int)
        out = chained(split_multiple(_updates, '\n', ',', atom_f=int),
            filter(lambda l: not in_dag(l, rules)),
            map(reorder_using(rules)),
            map(median),
            sum
        )
        return out


def subgraph(graph : list[tuple[int, int]], l):
    s = set(l)
    return [t for t in graph if t[0] in s and t[1] in s]


def reorder_using(graph):
    return lambda l: topological(subgraph(graph, l))


def median(l):
    return l[len(l) // 2]


def in_dag(l:list, rules):
    return all(l.index(f) < l.index(t) for f, t in rules if f in l and t in l)


def topological(edges : list[tuple[int, int]]):
    items = set(r[0] for r in edges) | set(r[1] for r in edges)
    adj = {item : list() for item in items}
    for fr, to in edges: adj[fr].append(to)
    ts = graphlib.TopologicalSorter(adj)
    return list(reversed(list(ts.static_order())))
