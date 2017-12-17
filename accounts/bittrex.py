from os import getenv
import bittrex


class Bittrex(object):
    def __init__(self, name, wallet):
        self.name = name
        self.wallet = wallet
        self.c = bittrex.Bittrex(
            getenv('BITTREX_API_KEY'), getenv('BITTREX_API_SECRET'))


    def market(self):
        return {
            "usdt": self.c.get_ticker("USDT-BTC")['result']['Bid'],
            "eth": self.c.get_ticker("BTC-ETH")['result']['Bid']
        }


    def balance(self, market):
        currencies = ['BTC', 'ETH']
        total = 0
        for c in currencies:
            result = self.c.get_balance(c)
            balance = result['result']['Balance']
            if balance == None: continue
            if c == 'BTC':
                ratio = 1
            else:
                ratio = market[c.lower()]

            value = market["usdt"] * float(ratio) * balance
            self.wallet.put(c, value)
            total += value
        return total
