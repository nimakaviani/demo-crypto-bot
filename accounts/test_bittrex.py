import pytest


@pytest.fixture
def bittrex():
    from accounts.bittrex import Bittrex
    from model.account import Wallet
    wallet = Wallet("nima")
    return Bittrex("bittrex", wallet)


@pytest.fixture(autouse=True)
def patch_fixture(monkeypatch):
    import bittrex

    def mock_ticker(self, currency):
        return {'result': {'Bid': 10}}

    def mock_balance(self, currency):
        return {'result': {'Balance': 10}}

    monkeypatch.setattr(bittrex.Bittrex, 'get_ticker', mock_ticker)
    monkeypatch.setattr(bittrex.Bittrex, 'get_balance', mock_balance)


def test_market(bittrex):
    m = bittrex.market()
    assert m["usdt"] == 10
    assert m["eth"] == 10


def test_balance(bittrex):
    balance = bittrex.balance({"usdt": 1, "eth": 2})
    assert balance == 30
