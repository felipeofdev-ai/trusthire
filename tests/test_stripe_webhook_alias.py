from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_stripe_webhook_alias_exists():
    r = client.post('/api/webhooks/stripe', data=b'{}')
    assert r.status_code in (400, 503)
