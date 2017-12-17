import pytest


@pytest.fixture
def currency():
    from model.account import Currency
    return Currency("test-currency", 10)


def test_update(currency):
    currency.update(15)
    assert currency.value == 25
