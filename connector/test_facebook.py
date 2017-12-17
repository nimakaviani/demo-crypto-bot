import pytest
from connector import facebook


@pytest.fixture
def vrequest():
    class Req:
        def __init__(self):
            self.args = dict()
            self.args["hub.mode"] = "subscribe"
            self.args["hub.challenge"] = "challenge"

    return Req()


@pytest.fixture
def patch_verify_token(monkeypatch):
    monkeypatch.setenv('FB_VERIFY_TOKEN', 'verification-token')


@pytest.mark.usefixtures("patch_verify_token")
def test_verify_fail(vrequest):
    resp = facebook.verify(vrequest)
    assert resp[0] == "Verification token mismatch"
    assert resp[1] == 403


@pytest.mark.usefixtures("patch_verify_token")
def test_verify_success(vrequest):
    vrequest.args['hub.verify_token'] = 'verification-token'
    resp = facebook.verify(vrequest)
    assert resp[0] == "challenge"
    assert resp[1] == 200


def test_verify_invalid(vrequest):
    del vrequest.args['hub.mode']
    resp = facebook.verify(vrequest)
    assert resp == None


@pytest.fixture
def hrequest():
    class Req:
        def __init__(self):
            self.messaging = [{
                "sender": {
                    "id": "sender-id"
                },
                "recipient": {
                    "id": "recipient-id"
                },
                "message": {
                    "text": "does this work?",
                    "seq": 20,
                    "mid": "mid.1466015596912:7348aba4de4cfddf91"
                },
                "timestamp": 1466015596919
            }]

        def get_json(self):
            return {
                "object":
                "page",
                "entry": [{
                    "id": "some-id",
                    "time": 1458692752478,
                    "messaging": self.messaging
                }]
            }

    return Req()


def test_handle_messaging(hrequest):
    resp = facebook.handle(hrequest)
    assert resp["sender"] == "sender-id"
    assert resp["message"] == "does this work?"


def test_handle_irrelavants(hrequest):
    hrequest.messaging = [{"delivery": {}}]
    resp = facebook.handle(hrequest)
    assert resp == None

    hrequest.messaging = [{"optin": {}}]
    resp = facebook.handle(hrequest)
    assert resp == None

    hrequest.messaging = [{"postback": {}}]
    resp = facebook.handle(hrequest)
    assert resp == None

    hrequest.messaging = [{"something-random": {}}]
    resp = facebook.handle(hrequest)
    assert resp == None


class MockResponse():
    def __init__(self, status_code):
        self.status_code = status_code


@pytest.fixture
def patch_requests(monkeypatch):
    import requests

    def patch_post(url, **args):
        assert "graph.facebook" in url
        assert "access_token" in args["params"]
        assert args["params"]["access_token"] == 'access-token-value'
        assert "message" in args["data"]
        assert "some-attachment" in args["data"]
        return MockResponse(200)

    monkeypatch.setattr(requests, "post", patch_post)


@pytest.fixture
def patch_access_token(monkeypatch):
    monkeypatch.setenv('FB_ACCESS_TOKEN', 'access-token-value')


@pytest.mark.usefixtures("patch_requests", "patch_access_token")
def test_send_message():
    message = {"attachment": "some-attachment"}
    facebook.send_message("some-recipient", message)


@pytest.mark.usefixtures("patch_access_token")
def test_send_message_exception(monkeypatch):
    import requests

    def patch_post(url, **args):
        return MockResponse(400)

    monkeypatch.setattr(requests, "post", patch_post)

    message = {"attachment": "some-attachment"}
    with pytest.raises(Exception):
        facebook.send_message("some-recipient", message)
