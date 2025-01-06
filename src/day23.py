from myutils import *


class Day23(AOC):
    EXPECTED1 = 7
    EXPECTED2 = "co,de,ka,ta"


    def part1(self, input: str) -> ...:
        edges: list[tuple[str, str]] = []
        vertices: set[str] = set()
        for line in input.strip().split('\n'):
            fr, to = line.split('-')
            edges.append((fr, to))
            vertices.add(fr)
            vertices.add(to)
        adjacency_map = {}
        for v in vertices:
            adjacency_map[v] = []
        for fr, to in edges:
            adjacency_map[fr].append(to)
            adjacency_map[to].append(fr)

        triples = set()
        for v1 in vertices:
            if v1[0] != 't': continue
            adj = adjacency_map[v1]
            for v2, v3 in itertools.product(adj, adj):
                if v3 in adjacency_map[v2]:
                    triples.add(tuple(sorted((v1, v2, v3))))
        print(triples)
        return len(triples)


    def part2(self, input: str) -> ...:
        edges: list[tuple[str, str]] = []
        vertices: set[str] = set()
        for line in input.strip().split('\n'):
            fr, to = line.split('-')
            edges.append((fr, to))
            vertices.add(fr)
            vertices.add(to)
        adjacency_map = {}
        for v in vertices:
            adjacency_map[v] = set()
        for fr, to in edges:
            adjacency_map[fr].add(to)
            adjacency_map[to].add(fr)

        return format(max(bron_kerbosch(adjacency_map), key=len))

def bron_kerbosch(graph, r=set(), p=None, x=set()):
    if p is None:
        p = set(graph.keys())
    if not p and not x:
        yield r
    else:
        u = next(iter(p | x))  # Choose a pivot vertex
        for v in p - graph[u]:
            yield from bron_kerbosch(graph, r | {v}, p & graph[v], x & graph[v])
            p.remove(v)
            x.add(v)

def format(s: set):
    items = sorted(s)
    return ','.join(items)