import pytest


@pytest.fixture
def coinbase():
    from accounts.coinbase import Coinbase
    from model.account import Wallet
    wallet = Wallet("nima")
    return Coinbase("coinbase", wallet)

@pytest.fixture(autouse=True)
def patch_fixture(monkeypatch):
    import coinbase.wallet.client

    def noop(self, api_key, api_secret, base_api_uri=None, api_versoin=None):
        pass
    def mock_account(self):
        return {
        "data":[
            {
            'currency': 'BTC',
            'balance': {
            'amount': 5
            }
            }, {
                'currency': 'ETH',
                'balance': {
                'amount': 10
                }
            }]
        }

    monkeypatch.setattr(coinbase.wallet.client.Client, 'get_accounts', mock_account)
    monkeypatch.setattr(coinbase.wallet.client.Client, '__init__', noop)


def test_market(coinbase):
    m = coinbase.market()
    assert m["BTC"] > 100
    assert m["ETH"] > 100
    assert m["LTC"] > 100


def test_balance(coinbase):
    m = coinbase.market()
    b = coinbase.balance(m)
    coinbase.wallet.ledger()
    assert coinbase.wallet.total > 0
    assert coinbase.wallet.gain > 0
