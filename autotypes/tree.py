from abc import ABC, abstractmethod
import ast
from typing import Any, Callable, Self

from autotypes.types import StrType, Type
from autotypes.rules import InvalidRuleApplication, rules

ast.AST.__str__ = lambda self: ast.dump(self)
ast.AST.__repr__ = lambda self: ast.dump(self)










class TypeDict(dict):
    def transform(self, key: ast.expr) -> str:
        class RemoveCtx(ast.NodeTransformer):
            def visit_Name(self, node: ast.Name) -> ast.Name:
                return ast.Name(id=node.id, ctx=ast.Load())

        key = RemoveCtx().visit(key)
        return ast.dump(key)

    def __getitem__(self, key: ast.expr) -> Type:
        return super().__getitem__(self.transform(key))

    def __setitem__(self, key: ast.expr, value: Type):
        return super().__setitem__(self.transform(key), value)

    def __contains__(self, key):
        return super().__contains__(self.transform(key))

with open("example.py") as f:
    code = f.read()

types: TypeDict[str, Type] = TypeDict()
types[ast.Name(id="input", ctx=ast.Load())] = StrType()


def get_type(node: ast.expr) -> Type:
    if node in types:
        return types[node]
    for rule in rules:
        try:
            expression_type = rule.apply(node, get_type)
            types[node] = expression_type
            return expression_type
        except InvalidRuleApplication:
            continue

    raise ValueError(f"Unable to determine the type of '{ast.unparse(node)}'")


module = ast.parse(code)
for assignment in module.body:
    match assignment:
        case ast.Assign(targets=targets, value=value):
            expression_type = get_type(value)
            for target in targets:
                if isinstance(target, ast.Name):
                    types[target] = expression_type

expression_types = {}
