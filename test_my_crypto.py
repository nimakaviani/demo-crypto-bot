import pytest
import os

# integration tests
@pytest.fixture
def my_crypto_no_watson(capsys, monkeypatch):
    from helpers.notifier import Notifier
    from my_crypto import MyCrypto

    def patched_report(self, recipient_id, wallet, time):
        assert recipient_id == "sender-id"

    def patched_quick_reply(self, recipient_id, msg):
        assert recipient_id == "sender-id"
        assert ('balance' in msg or 'account' in msg)

    monkeypatch.setattr(Notifier, "quick_reply", patched_quick_reply)
    monkeypatch.setattr(Notifier, "balance", patched_report)

    return MyCrypto()

@pytest.mark.usefixtures("my_crypto_no_watson")
def test_handle(my_crypto_no_watson):
    response = {"sender": "sender-id", "message": "balance"}
    my_crypto_no_watson.handle(response)
