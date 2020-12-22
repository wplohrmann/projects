from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import TextInput, Text, Paragraph, Div
from bokeh.plotting import figure
from manual import FoodGraph
import re
from time import time


title = "Kimchi scrambled eggs on toast"
graph = FoodGraph(title)
steps = """Beat the eggs and milk together with a pinch of salt. Pour into a non-stick pan over a low heat. Leave untouched for 30 seconds, then lift the pan a little and swirl the eggs around. Cook for 2 mins more, then fold through the kimchi, breaking up the eggs to scramble them. Serve the kimchi scrambled eggs on the toast, and top with the spring onion and tograshi, if using.
"""
steps = re.findall("[^\.,]+[\.,]", steps)
state=  {"div": 0}

def update_graph(attr, old, new):
    print("New:", new)
    graph.parse_input(new)
    state["div"] += 1
    path = f'app/static/haha{state["div"]}'
    graph.dot.render(path)
    image.text = f'<img src="{path}.png"/>'
    image.width = graph.render().shape[1]

selected_line = TextInput(title="Line", value="0")
command = TextInput(title="Command")
command.on_change("value", update_graph)
instructions = column(*[Paragraph(text=step) for step in steps])

image = Div()
curdoc().title = "Text2Graph"
top_row = row(image, instructions)
root = column(top_row, command)
curdoc().add_root(root)
