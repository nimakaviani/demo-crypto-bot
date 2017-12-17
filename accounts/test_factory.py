import pytest

@pytest.fixture(autouse=True)
def factory():
    from model.account import Wallet
    from accounts.factory import Factory
    wallet = Wallet("test")
    return Factory(wallet)

def test_gemini(factory, monkeypatch):
    from accounts import gemini
    monkeypatch.setenv('GEMINI_API_KEY', 'key')
    monkeypatch.setenv('GEMINI_API_SECRET', 'secret')

    account = factory.create('gemini')
    assert isinstance(account, gemini.Gemini)


def test_gemini_noenv(factory, monkeypatch, capsys):
    monkeypatch.delenv('GEMINI_API_KEY', 'key')
    monkeypatch.delenv('GEMINI_API_SECRET', 'secret')

    account = factory.create('gemini')
    captured = capsys.readouterr()
    assert 'env vars for gemini not present' in captured.out


def test_coinbase(factory, monkeypatch):
    from accounts import coinbase
    monkeypatch.setenv('COINBASE_API_KEY', 'key')
    monkeypatch.setenv('COINBASE_API_SECRET', 'secret')

    account = factory.create('coinbase')
    assert isinstance(account, coinbase.Coinbase)


def test_coinbase_noenv(factory, monkeypatch, capsys):
    monkeypatch.delenv('COINBASE_API_KEY', 'key')
    monkeypatch.delenv('COINBASE_API_SECRET', 'secret')

    account = factory.create('coinbase')
    captured = capsys.readouterr()
    assert 'env vars for coinbase not present' in captured.out


def test_bittrex(factory, monkeypatch):
    from accounts import bittrex
    monkeypatch.setenv('BITTREX_API_KEY', 'key')
    monkeypatch.setenv('BITTREX_API_SECRET', 'secret')

    account = factory.create('bittrex')
    assert isinstance(account, bittrex.Bittrex)


def test_bittrex_noenv(factory, monkeypatch, capsys):
    monkeypatch.delenv('BITTREX_API_KEY', 'key')
    monkeypatch.delenv('BITTREX_API_SECRET', 'secret')

    account = factory.create('bittrex')
    captured = capsys.readouterr()
    assert 'env vars for bittrex not present' in captured.out

