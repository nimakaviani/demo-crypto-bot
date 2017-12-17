import pytest


@pytest.fixture
def gemini():
    from accounts.gemini import Gemini
    from model.account import Wallet
    wallet = Wallet("nima")
    return Gemini("gemini", wallet)


@pytest.fixture(autouse=True)
def patch_fixture(monkeypatch):
    import gemini.client

    def mock_ticker(self, currency):
        return {'last': 10}

    def mock_balance(self):
        return [{
            'currency': 'BTC',
            'amount': 5
        }, {
            'currency': 'ETH',
            'amount': 10
        }]

    monkeypatch.setattr(gemini.client.Client, 'get_ticker', mock_ticker)
    monkeypatch.setattr(gemini.client.Client, 'get_balance', mock_balance)


def test_market(gemini):
    m = gemini.market()
    assert m["btcusd"] == 10
    assert m["ethusd"] == 10


def test_balance(gemini):
    balance = gemini.balance({"btcusd": 2, "ethusd": 3})
    assert balance == 40
