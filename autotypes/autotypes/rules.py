from abc import ABC, abstractmethod
import ast
from typing import Any, Callable, Self

from autotypes.types import IntType, StrType, Type
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

class Rule(ABC):
    @abstractmethod
    def apply(self, node: ast.expr, get_type: Callable[[ast.expr], Type]) -> Type:
        raise NotImplementedError


class InvalidRuleApplication(Exception):
    pass


class AddIntsOrStr(Rule):
    pattern: ast.BinOp = ast.parse("_a + _b", mode="eval").body

    def apply(self, node: ast.expr, get_type: Callable[[ast.expr], Type]) -> Type:
        matched = match_ast(self.pattern, node)
        if matched is False:
            raise InvalidRuleApplication
        type_a = get_type(matched[self.pattern.left])
        type_b = get_type(matched[self.pattern.right])
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

    def apply(self, node: ast.expr, get_type: Callable[[ast.expr], Type]) -> Type:
        matched = match_ast(self.pattern, node)
        if matched is False:
            raise InvalidRuleApplication
        func = matched[self.pattern.func]

        return get_type(func)


class Constant(Rule):
    pattern = ast.Constant(ast.Name("_value"))

    def apply(self, node: ast.expr, get_type: Callable[[ast.expr], Type]) -> type:
        matched = match_ast(self.pattern, node)
        if matched is False:
            raise InvalidRuleApplication
        value = matched[self.pattern.value]
        if isinstance(value, int):
            return IntType()
        elif isinstance(value, str):
            return StrType()

rules: list[Rule] = [AddIntsOrStr(), Call(), Constant()]
