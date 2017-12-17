from os import getenv
from accounts import bittrex
from accounts import gemini
from accounts import coinbase


class Factory(object):
    def __init__(self, wallet):
        self.wallet = wallet
        self.err_msg = """env vars for {} not present. if no {} account, remove the account name from `ACCOUNTS` in my_crypto.py"""


    def create(self, type):
        if type == "gemini":
            if getenv('GEMINI_API_KEY') and getenv('GEMINI_API_SECRET'):
                return gemini.Gemini(type, self.wallet)
            else:
                print(self.err_msg.format(type, type))
        if type == "bittrex":
            if getenv('BITTREX_API_KEY') and getenv('BITTREX_API_SECRET'):
                return bittrex.Bittrex(type, self.wallet)
            else:
                print(self.err_msg.format(type, type))
        if type == "coinbase":
            if getenv("COINBASE_API_KEY") and getenv("COINBASE_API_SECRET"):
                return coinbase.Coinbase(type, self.wallet)
            else:
                print(self.err_msg.format(type, type))
