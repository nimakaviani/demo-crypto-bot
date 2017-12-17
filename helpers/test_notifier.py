import pytest
from datetime import datetime

current_time = datetime.now()


@pytest.fixture
def patch_facebook(monkeypatch):
    import connector.facebook

    def send_message(recipient_id, data):
        assert recipient_id == 'recipient-id'
        elements = data['attachment']['payload']['elements']
        validate_existance(elements[0]['title'], 'Summary')
        validate_existance(elements[0]['title'], '30')
        validate_existance(elements[0]['subtitle'], 'Total: 30')
        validate_existance(elements[0]['subtitle'], 'Gain: 30')
        validate_existance(elements[1]['title'], 'currency-1')
        validate_existance(elements[1]['subtitle'], 'Value: 10')
        validate_existance(elements[1]['subtitle'], 'Gain: 10')
        validate_existance(elements[1]['image_url'], 'currency-1.png')
        validate_existance(elements[2]['title'], 'currency-2')
        validate_existance(elements[2]['subtitle'], 'Value: 20')
        validate_existance(elements[2]['subtitle'], 'Gain: 20')
        validate_existance(elements[2]['image_url'], 'currency-2.png')

    monkeypatch.setattr(connector.facebook, 'send_message', send_message)


@pytest.fixture
def notifier():
    from helpers.notifier import Notifier
    return Notifier()


@pytest.mark.usefixtures("patch_facebook", "notifier")
def test_balance(notifier):
    from model.account import Wallet
    wallet = Wallet("nima")
    wallet.put("currency-1", 10)
    wallet.put("currency-2", 20)
    notifier.balance("recipient-id", wallet, current_time)


def validate_existance(actual, expected):
    assert expected in actual
