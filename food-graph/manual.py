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

    def add_edge(self, label, start=None, stop=None):
        if start is None:
            start = self.last_node
            assert stop is None
            stop = start + "'"
        assert stop is not None
        if start not in self.nodes:
            self.add_node(start)
        if stop not in self.nodes:
            self.add_node(stop)
        self.last_node = stop
        print(f"{start} ==({label})==> {stop}")
        self.dot.edge(self.nodes[start], self.nodes[stop], label)

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
        if s == "":
            return False
        tree = self.lark.parse(s)
        print(tree.pretty())
        start = stop = None
        for word in tree.children:
            value = word.children[0].value.strip("()")
            if word.data == "action":
                action = value
            elif word.data == "start":
                start = value
            elif word.data == "stop":
                stop = value

        self.add_edge(action, start, stop)

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
