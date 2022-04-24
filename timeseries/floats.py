from __future__ import annotations
from dataclasses import dataclass
from typing import TypeVar, Union, overload

T = TypeVar("T", bound="Float")

@dataclass
class Float:
    value: float
    def __add__(self: T, other: T) -> T:
        return self.__class__(self.value + other.value)

    def __sub__(self: T, other: T) -> T:
        return self.__class__(self.value - other.value)

    def __ge__(self: T, other: T) -> bool:
        return self.value >= other.value
    def __neg__(self: T) -> T:
        return self.__class__(-self.value)

class Price(Float):
    def __mul__(self, stock: Stock) -> Currency:
        return Currency(self.value * stock.value)
    def __str__(self) -> str:
        return f"£{self.value} per share"

class Currency(Float):
    @overload
    def __truediv__(self, other: Stock) -> Price: ...

    @overload
    def __truediv__(self, other: Price) -> Stock: ...

    def __truediv__(self, other: Union[Stock, Price]) -> Union[Price, Stock]:
        if isinstance(other, Stock):
            return Price(self.value / other.value)
        else:
            return Stock(self.value / other.value)

    def __str__(self) -> str:
        return f"£{self.value}"

class Stock(Float):
    def __mul__(self, price: Price) -> Currency:
        return Currency(self.value * price.value)

    def __str__(self) -> str:
        return f"{self.value} shares"


if __name__ == "__main__":
    currency = Currency(5)
    stock = Stock(5)
    price = Price(1)

    currency / stock, price
    price * stock, currency
    currency / price, stock
    stock + stock
    # stock + price
    price + price
