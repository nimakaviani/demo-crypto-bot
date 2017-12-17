import pytest
from model.account import Currency


@pytest.fixture
def wallet():
    from model.account import Wallet
    return Wallet("test")


def test_currency_put(wallet):
    wallet.put("currency", 10)
    assert wallet.wallet["currency"].value == 10
    wallet.put("currency", 20)
    assert len(wallet.items()) == 1
    assert wallet.wallet["currency"].value == 30


def test_items(wallet):
    wallet.put("currency", 10)
    assert len(wallet.items()) == 1
    for i, currency in wallet.items():
        assert currency.name == "currency"
        assert currency.value == 10


def test_ledger(wallet):
    wallet.put("currency-1", 10)
    wallet.put("currency-2", 15)
    assert len(wallet.items()) == 2
    output = wallet.ledger()
    assert "currency-1" in output
    assert "\t value: 10" in output
    assert "\t gain: 10" in output
    assert "currency-2" in output
    assert "\t value: 15" in output
    assert "\t gain: 15" in output
    assert "\t total: 25" in output
    assert "\t gain: 25" in output


def test_ledger(wallet):
    wallet.put("currency-1", 10)
    wallet.put("currency-2", 20)
    assert len(wallet.items()) == 2
    output = wallet.ledger()
    assert "currency-1" in output
    assert "\t value: 10" in output
    assert "\t gain: 10" in output
    assert "currency-2" in output
    assert "\t value: 20" in output
    assert "\t gain: 20" in output
    assert "\t total: 30" in output
    assert "\t gain: 30" in output
    wallet.reset()
    wallet.put("currency-1", 15)
    wallet.put("currency-2", 10)
    assert len(wallet.items()) == 2
    output = wallet.ledger()
    assert "currency-1" in output
    assert "\t value: 15" in output
    assert "\t gain: 5" in output
    assert "currency-2" in output
    assert "\t value: 10" in output
    assert "\t gain: -10" in output
    assert "\t total: 25" in output
    assert "\t gain: -5" in output
