import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

from myutils import *


class Day24(AOC):
    EXPECTED1 = 2024

    def parse(self, input):
        inputs = {}
        gates = {}
        _inputs, _gates = input.strip().split('\n\n')
        z_max = 0
        for line in _inputs.split('\n'):
            name, val = line.split(': ')
            inputs[name] = val
        for line in _gates.split('\n'):
            x, gate, y, _, z = line.split(' ')
            gates[z] = (x, gate, y)
            if z[0] == 'z':
                z_max = max(z_max, int(z[1:]))
        return inputs, gates, z_max


    def part1(self, input: str) -> ...:
        inputs, gates, z_max = self.parse(input)

        def calc(g):
            if g[0] in {'x', 'y'}: return int(inputs[g])
            x, gate, y = gates[g]
            return functions[gate](calc(x), calc(y))
        out = convert(z_max, 'z', calc)

        return out

    def part2(self, input: str) -> ...:
        if len(input) < 1000: return
        inputs, gates, z_max = self.parse(input)

        # done manually, code below to validate and generate answer
        swap(gates, 'vvr', 'z08')
        swap(gates, 'tfb', 'z28')
        swap(gates, 'rnq', 'bkr')
        swap(gates, 'mqh', 'z39')

        return ','.join(sorted([
            'vvr', 'z08',
            'tfb', 'z28',
            'rnq', 'bkr',
            'mqh', 'z39'
        ]))

functions = {
    "XOR": lambda a, b: a ^ b,
    "OR": lambda a, b: a | b,
    "AND": lambda a, b: a & b,
}


def convert(length, c, value_provider):
    num = ''
    for i in range(length, -1, -1):
        s = c + str(i).rjust(2, '0')
        num += str(value_provider(s))
    return int(num, base=2)


def to_binary_string(i):
    return str("{0:b}".format(i))


def draw_graph(gates):
    label_dict = {}
    G = nx.DiGraph()
    for z, ins in gates.items():
        x, gate, y = ins
        G.add_edge(z, x)
        G.add_edge(z, y)
        if z[0] == 'z':
            G.add_edge("_out"+z, z)
            label_dict["_out"+z] = z
            label_dict[z] = gate
        else:
            label_dict[z] = f"{gate}\n{z}"
        if x[0] in 'xyz': label_dict[x] = x
        if y[0] in 'xyz': label_dict[y] = y

    plt.figure(1, figsize=(60, 120), dpi=60)
    pos = graphviz_layout(G, prog="dot")

    values = [color(v) for v in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_color=values, node_size=500)
    nx.draw_networkx_labels(G, pos, labels=label_dict)
    nx.draw_networkx_edges(G, pos, edge_color='r', arrows=True)
    nx.draw_networkx_edges(G, pos, arrows=False)
    plt.show()


def color(v):
    if v[0] == '_': return 'purple'
    if v[0] == 'x': return 'red'
    if v[0] == 'y': return 'blue'
    return 'gray'


def swap(dict, a, b):
    dict[a], dict[b] = dict[b], dict[a]