from fastapi import FastAPI
from fastapi.testclient import TestClient

from utils.security import SecurityHeadersMiddleware


def test_security_headers_present():
    app = FastAPI()
    app.add_middleware(SecurityHeadersMiddleware)

    @app.get("/ok")
    def ok():
        return {"status": "ok"}

    client = TestClient(app)
    response = client.get("/ok")

    assert response.status_code == 200
    assert response.headers.get("content-security-policy") is not None
    assert response.headers.get("x-content-type-options") == "nosniff"
    assert response.headers.get("x-frame-options") == "DENY"
