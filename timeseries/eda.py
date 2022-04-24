import csv
from datetime import date
from typing import List, cast

import numpy as np
import matplotlib.pyplot as plt

from floats import Currency, Price, Stock



prices: List[Price] = []
dates: List[date] = []
with open("TSLA.csv") as f:
    reader = csv.reader(f)
    header = next(reader)
    date_column = header.index("Date")
    price_column = header.index("Open")
    for row in reader:
        dates.append(date(*map(int, row[date_column].split("-"))))
        prices.append(Price(float(row[price_column])))


# plt.plot(dates, prices)
# plt.show()

class Model:
    def step(self, price: Price, stocks: Stock, available: Currency) -> Stock:
        """
        Given a current stock price `price`, amount of stocks `stocks` and money available
        `available`, return the amount of stock to buy (positive) or sell (negative). Buying
        more stock than you have money for or selling more than you have raises an assertion error.
        """
        raise NotImplementedError

class Evaluator:
    def __init__(self, prices: List[Price]):
        self.prices = prices

    def evaluate(self, model: Model) -> Currency:
        stocks = Stock(0)
        available = Currency(1)
        for price in self.prices:
            amount = model.step(price, stocks, available)
            stocks = stocks + amount
            available = available - amount * price
            assert stocks >= Stock(0)
            assert available >= Currency(-1e-9)
            if amount.value > 0:
                print(f"Bought {amount} at {price}. Currently available: {available}")
            elif amount.value < 0:
                print(f"Sold {amount} at {price}. Currently available: {available}")
        # Sell everything at the end of the period
        available += stocks * price

        return available - Currency(1)


class BuyOnce(Model):
    def __init__(self) -> None:
        self.bought = False

    def __str__(self) -> str:
        return f"BuyOnce()"

    def step(self, price: Price, stocks: Stock, available: Currency) -> Stock:
        if self.bought:
            return Stock(0)
        else:
            self.bought = True
            return available / price

class SMA(Model):
    def __init__(self, short: int, long: int):
        self.historical: List[float] = []
        assert short < long
        self.short = short
        self.long = long

    def __str__(self) -> str:
        return f"SMA(long={self.long}, short={self.short})"

    def step(self, price: Price, stocks: Stock, available: Currency) -> Stock:
        self.historical.append(price.value)
        if len(self.historical) < self.long:
            return Stock(0)
        long_average = cast(float, np.mean(self.historical[-self.long:]))
        short_average = cast(float, np.mean(self.historical[-self.short:]))
        if short_average > long_average:
            # Buy as much as possible 🚀
            return available / price
        else:
            # Sell everything
            return -stocks



rise = prices[-1] - prices[0]
correction  = np.linspace(0, rise.value, len(prices))
prices = [price - Price(x) for price, x in zip(prices, correction)]
evaluator = Evaluator(prices)

models = [BuyOnce(), SMA(5, 10), SMA(50, 100), SMA(1, 3), SMA(10, 20)]
profits = {}
for model in models:
    print(f"===={model}====")
    profits[str(model)] = evaluator.evaluate(model)

print("="*10 + " Summary " + "="*10)
for model_name, profit in profits.items():
    print(f"Model {model_name}, Profit: {profit}")

