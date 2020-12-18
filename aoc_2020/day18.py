import re
import ast
p = "day18.txt"
with open(p) as f:
    lines = f.readlines()

class DivToAdd(ast.NodeTransformer):
    def visit_Div(self, node):
        return ast.Add()

s= 0
for line in lines:
    swapped = line.strip().replace("+","/")
    tree = ast.parse(swapped, mode="eval")
    tree = DivToAdd().generic_visit(tree)
    val = eval(compile(tree, "", mode="eval"))
    s += val
print("Final answer:", s)

class SwapAddMult(ast.NodeTransformer):
    def visit_Mult(self, node):
        return ast.Add()
    def visit_Add(self, node):
        return ast.Mult()

s= 0
for line in lines:
    swapped = line.strip().translate(str.maketrans({"*":"+","+":"*"}))
    tree = ast.parse(swapped, mode="eval")
    tree = SwapAddMult().generic_visit(tree)
    val = eval(compile(tree, "", mode="eval"))
    s += val
print("Final answer:", s)

