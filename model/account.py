import logging
import copy

logger = logging.getLogger(__name__)


class Currency(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def update(self, new_value):
        self.value += new_value


class Wallet(object):
    def __init__(self, name):
        self.name = name
        self.wallet = dict()


    def put(self, name, value):
        if name in self.wallet:
            self.wallet[name].update(value)
        else:
            self.wallet[name] = Currency(name, value)


    def reset(self):
        self.old_wallet = copy.deepcopy(self.wallet)
        self.wallet = dict()


    def items(self):
        tmp = dict()
        for n in self.wallet:
            c = self.wallet[n]
            if c.value == 0.0:
                continue
            tmp[n] = c
        return tmp.items()


    def ledger(self):
        ledger_output = ""
        self.total = 0
        self.gain = 0
        for name, currency in self.wallet.items():
            try:
                old_value = self.old_wallet[name].value
                currency.gain = currency.value - old_value
            except:
                currency.gain = currency.value
            self.gain += currency.gain
            self.total += currency.value
            ledger_output += "{} \n".format(currency.name)
            ledger_output += "\t value: {} \n".format(str(currency.value))
            ledger_output += "\t gain: {} \n\n".format(str(currency.gain))

        ledger_output += "------- \n"
        ledger_output += "\t total: {} \n".format(str(self.total))
        ledger_output += "\t gain: {} \n".format(str(self.gain))
        return ledger_output


    def ledger_html(self):
        return self.ledger().replace("\n", "<br/>").replace("\t", 8 * " ")
