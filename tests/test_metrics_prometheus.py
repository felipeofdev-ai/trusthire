from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_prometheus_metrics_endpoint():
    r = client.get('/metrics/prometheus')
    assert r.status_code == 200
    assert 'trusthire_uptime_percent' in r.text
    assert r.headers['content-type'].startswith('text/plain')
