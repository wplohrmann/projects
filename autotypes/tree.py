from abc import ABC, abstractmethod
import ast
from typing import Any, Callable, Self

ast.AST.__str__ = lambda self: ast.dump(self)
ast.AST.__repr__ = lambda self: ast.dump(self)


def match_ast(pattern, target):
    """Recursively check if `target` matches the `pattern` structure."""
    if isinstance(pattern, ast.AST) and isinstance(target, ast.AST):
        if type(pattern) is not type(target):
            return False

        matched_vars = {}

        for field in pattern._fields:
            p_val = getattr(pattern, field, None)
            t_val = getattr(target, field, None)

            if isinstance(p_val, ast.Name) and p_val.id.startswith("_"):
                matched_vars[p_val] = t_val
            elif isinstance(p_val, ast.AST):
                submatch = match_ast(p_val, t_val)
                if submatch is False:
                    return False
                matched_vars.update(submatch)

            elif isinstance(p_val, list):
                if not isinstance(t_val, list) or len(p_val) != len(t_val):
                    return False
                for p_item, t_item in zip(p_val, t_val):
                    submatch = match_ast(p_item, t_item)
                    if submatch is False:
                        return False
                    matched_vars.update(submatch)

            elif p_val != t_val:
                return False

        return matched_vars

    return False


class Type(ABC):
    @classmethod
    @abstractmethod
    def is_type(self, value: Any) -> Self:
        raise NotImplementedError


class IntType(Type):
    @classmethod
    def is_type(cls, value: Any) -> Self:
        if isinstance(value, int):
            return cls
        raise ValueError(f"{value} is not an int")

    def __str__(self):
        return "int"


class StrType(Type):
    @classmethod
    def is_type(cls, value: Any) -> Self:
        if isinstance(value, str):
            return cls
        raise ValueError(f"{value} is not a str")

    def __str__(self):
        return "str"


class Rule(ABC):
    @property
    @abstractmethod
    def pattern(self) -> ast.expr:
        raise NotImplementedError

    @abstractmethod
    def apply(self, node: ast.expr, get_type: Callable[[ast.expr], Type]) -> Type:
        raise NotImplementedError


class InvalidRuleApplication(Exception):
    pass


class AddIntsOrStr(Rule):
    pattern = ast.parse("_a + _b", mode="eval").body

    def apply(self, node: ast.expr, get_type: Callable[[ast.expr], Type]) -> type:
        matched = match_ast(self.pattern, node)
        if matched is False:
            raise InvalidRuleApplication
        type_a = get_type(matched["_a"])
        type_b = get_type(matched["_b"])
        if type(type_a) != type(type_b):
            raise InvalidRuleApplication
        elif isinstance(type_a, IntType):
            return IntType()
        elif isinstance(type_a, StrType):
            return StrType()
        else:
            raise InvalidRuleApplication


class Call(Rule):
    pattern: ast.Call = ast.parse("_func()", mode="eval").body

    def apply(self, node: ast.expr, get_type: Callable[[ast.expr], Type]) -> type:
        matched = match_ast(self.pattern, node)
        if matched is False:
            raise InvalidRuleApplication
        func = matched[self.pattern.func]
        if func not in types:
            breakpoint()
            print
            raise ValueError(f"Unknown function '{func}'")
        return types[func]


class Constant(Rule):
    pattern = ast.Constant("_value")

    def apply(self, node: ast.expr, get_type: Callable[[ast.expr], Type]) -> type:
        matched = match_ast(self.pattern, node)
        if matched is False:
            raise InvalidRuleApplication
        value = matched["_value"]
        if isinstance(value, int):
            return IntType()
        elif isinstance(value, str):
            return StrType()


with open("example.py") as f:
    code = f.read()

rules: list[Rule] = [AddIntsOrStr(), Call(), Constant()]


class TypeDict(dict):
    def __getitem__(self, key: ast.expr) -> Type:
        return super().__getitem__(ast.dump(key))

    def __setitem__(self, key: ast.expr, value: Type):
        return super().__setitem__(ast.dump(key), value)

    def __contains__(self, key):
        return super().__contains__(ast.dump(key))


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
