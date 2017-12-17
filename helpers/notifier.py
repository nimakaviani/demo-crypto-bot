import json
from os import getenv
from connector import facebook

FMT = "%Y-%m-%d %H:%M:%S"


class Notifier(object):
    def balance(self, recipient_id, wallet, time):
        wallet.ledger()
        report = list()
        report.append({
            "title":
            "Summary - \n\n" + str(wallet.total),
            "image_url":
            "http://cdn.onlinewebfonts.com/svg/download_261825.png",
            "subtitle":
            "Date: " + time.strftime(FMT) + " \n\n Total: " +
            str(wallet.total) + " \n\n Gain: " + str(wallet.gain)
        })

        for name, currency in wallet.items():
            url = "https://github.com/cjdowner/cryptocurrency-icons/raw/master/128/black/{}.png".format(
                currency.name.lower())
            if name == "USD":
                url = "https://cdn.onlinewebfonts.com/svg/img_457962.png"
            report.append({
                "title":
                currency.name,
                "image_url":
                url,
                "subtitle":
                "Value: " + str(currency.value) + " \n\n Gain: " +
                str(currency.gain)
            })

        data = json.load(open("templates/notifier.json", 'r'))
        data["attachment"]["payload"]["elements"] = report
        facebook.send_message(recipient_id, data)


    def quick_reply(self, recipient_id, message):
        facebook.send_message(recipient_id, {"text": message})
