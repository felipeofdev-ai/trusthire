from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_system_health_endpoint():
    r = client.get('/system/health')
    assert r.status_code == 200
    data = r.json()
    assert 'uptime' in data
    assert 'latency' in data
    assert 'ai_accuracy' in data
    assert 'threats_blocked' in data
