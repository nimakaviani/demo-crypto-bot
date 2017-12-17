from os import getenv
import requests
from coinbase.wallet.client import Client


class Coinbase(object):
    def __init__(self, name, wallet):
        self.name = name
        self.wallet = wallet
        self.c = Client(
            getenv("COINBASE_API_KEY"), getenv("COINBASE_API_SECRET"))


    def balance(self, market):
        accounts = self.c.get_accounts()
        for account in accounts["data"]:
            if account["currency"] == "USD":
                rate = 1.0
            else:
                rate = market[account["currency"]]
            self.wallet.put(account["currency"],
                            rate * float(account["balance"]["amount"]))


    def market(self):
        market = dict()
        symbols = ['BTC', 'ETH', 'LTC']
        for symbol in symbols:
            resp = requests.get(
                "https://api.coinbase.com/v2/prices/{}-USD/buy".format(symbol))
            result = resp.json()
            market[symbol] = float(result['data']['amount'])
        return market
