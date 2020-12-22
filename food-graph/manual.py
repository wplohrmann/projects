import re
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from graphviz import Digraph
from lark import Lark

class FoodGraph:
    def __init__(self, title):
        self.dot = Digraph(title, format="png")
        k = 65
        self.alphabet = list(map(chr, range(k, k+26)))
        self.nodes = {}
        self.last_node = None
        self.lark = Lark(open("instructions.lark").read(), start="command")

    def add_node(self, label):
        letter = self.alphabet.pop()
        self.nodes[label] = letter
        self.dot.node(letter, label)

    def add_edge(self, label, n1=None, n2=None):
        if n1 is None:
            n1 = self.last_node
            assert n2 is None
            n2 = n1 + "'"
        assert n2 is not None
        if n1 not in self.nodes:
            self.add_node(n1)
        if n2 not in self.nodes:
            self.add_node(n2)
        self.last_node = n2
        print(f"{n1} ==({label})==> {n2}")
        self.dot.edge(self.nodes[n1], self.nodes[n2], label)

    def show(self):
        b = BytesIO(self.dot.pipe())
        arr = plt.imread(b)
        plt.imshow(arr)
        plt.show()

    def parse_input(self, s):
        """
        Parse a string and add nodes and edges to the graph. Return True if graph modified
        Grammar:
        `action` `start` to `stop`: Add edge `action` from `start` to `stop`
        `action`: Add edge `action` from last `stop` to `stop`'
        `action` to `stop`: Add edge `action` from last `stop` to `stop`

        Each keyword may contain non-whitespace characters, or whitespace characters if surrounded by parentheses
        """
        words = re.split(" (?!.*?\))", s)
        tree = self.lark.parse(s)
        print(tree.pretty())
        import pdb; pdb.set_trace()

        if len(words) == 1:
            self.add_edge(words[0])
            return True
        if len(words) != 3:
            return False
        action, n1, n2 = words
        self.add_edge(action, n1, n2)
        return True

title = "Kimchi scrambled eggs on toast"
graph = FoodGraph(title)
steps = """Beat the eggs and milk together with a pinch of salt. Pour into a non-stick pan over a low heat. Leave untouched for 30 seconds, then lift the pan a little and swirl the eggs around. Cook for 2 mins more, then fold through the kimchi, breaking up the eggs to scramble them. Serve the kimchi scrambled eggs on the toast, and top with the spring onion and tograshi, if using.
"""
steps = re.findall("[^\.,]+[\.,]", steps)
for i, step in enumerate(steps):
    print(f"Step {i}:", step)
    while graph.parse_input(input()):
        pass

graph.show()
