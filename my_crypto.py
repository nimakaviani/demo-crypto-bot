import bittrex
import os
from time import sleep
from pytz import timezone
from datetime import datetime
from model.account import Wallet
from helpers import notifier
from os import getenv
from accounts import factory
import watson_developer_cloud

ACCOUNTS = ['gemini', 'bittrex', 'coinbase']

class MyCrypto(object):
    def __init__(self):
        self.wallet = Wallet("nima")
        self.factory = factory.Factory(self.wallet)
        self.notify = notifier.Notifier()

        self.accounts = dict()
        for account_name in ACCOUNTS:
            acc = self.factory.create(account_name)
            if acc != None:
                self.accounts[account_name] = acc

        if os.getenv('ENABLE_WATSON') and os.getenv('ENABLE_WATSON').lower() == 'true':
            if os.getenv('WATSON_CONVERSATION_USERNAME') and os.getenv('WATSON_CONVERSATION_PASSWORD') and os.getenv('WATSON_CONVERSATION_WORKSPACE'):
                self.conversation = watson_developer_cloud.ConversationV1(
                    username=getenv('WATSON_CONVERSATION_USERNAME'),
                    password=getenv('WATSON_CONVERSATION_PASSWORD'),
                    version='2017-05-26')
                self.workspace_id = getenv('WATSON_CONVERSATION_WORKSPACE')
            else:
                print('failed to connecto to watson')


    def handle(self, response):
        if response == None:
            return

        recipient_id = response["sender"]
        message_text = response["message"]

        if os.getenv('ENABLE_WATSON') and os.getenv('ENABLE_WATSON').lower() == 'true':
            self.__watsonize(recipient_id, message_text)
        elif message_text.lower() == 'balance':
            self.__capture_summary(recipient_id)

        self.__report_balance(recipient_id, self.wallet)
        self.wallet.reset()


    def __assess(self, account):
        try:
            print("getting balance for {}...".format(account.name))
            market = account.market()
            account.balance(market)
        except Exception as e:
            print("{} market failed".format(account.name))
            print("errror: {}".format(e))


    def __capture_summary(self, recipient_id):
        for name, account in self.accounts.items():
            self.__assess(account)


    def __watsonize(self, recipient_id, message_text):
        response = self.__process_user_input(message_text)
        if response['output']['text']:
            self.notify.quick_reply(recipient_id, response['output']['text'][0])

        if response['intents']:
            intent = response['intents'][0]['intent']
            if intent == "balance":
                if not response['entities']:
                    self.__capture_summary()
                else:
                    entity = response['entities'][0]['value']
                    self.__assess(self.accounts[entity])


    def __process_user_input(self, user_input):
        response = self.conversation.message(
            workspace_id=self.workspace_id,
            input={'text': user_input},
            context={}
        )
        print(response)
        return response


    def __report_balance(self, recipient_id, wallet):
        time = datetime.now(timezone('UTC')).astimezone(timezone('US/Pacific'))
        self.notify.balance(recipient_id, wallet, time)
