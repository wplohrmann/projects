from abc import ABC, abstractmethod
from typing import Any, Dict, Self


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


class FuncType(Type):
    @classmethod
    def is_type(cls, value: Any) -> Self:
        if callable(value):
            return cls
        raise ValueError(f"{value} is not a function")

    def get_return_type(self, args: Dict[str, Type]) -> Type:
        raise NotImplementedError

    def __str__(self):
        return "function"
