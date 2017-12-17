from os import getenv
from gemini.client import Client


class Gemini(object):
    def __init__(self, name, wallet):
        self.name = name
        self.wallet = wallet
        self.c = Client(getenv('GEMINI_API_KEY'), getenv('GEMINI_API_SECRET'))


    def balance(self, market):
        balances = self.c.get_balance()
        total = 0

        for balance in balances:
            currency = balance['currency']
            rate = market["btcusd"]
            if currency == "USD":
                rate = 1.0
            if currency == "ETH":
                rate = market["ethusd"]

            value = float(balance['amount']) * rate
            self.wallet.put(currency, value)
            total += value
        return total


    def market(self):
        market = dict()
        symbols = ["btcusd", "ethusd", "ethbtc"]
        for symbol in symbols:
            result = self.c.get_ticker(symbol)
            market[symbol] = float(result['last'])
        return market
