from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_resume_optimize_json():
    payload = {
        "resume_text": "Senior Python engineer with FastAPI, Docker, and AWS experience. Delivered APIs and reduced latency.",
        "job_description": "Looking for Python FastAPI engineer with AWS, PostgreSQL, Redis and strong communication.",
        "ats_provider": "workday",
        "output_format": "json",
    }
    r = client.post("/api/v1/resume/optimize", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["provider"] == "workday"
    assert isinstance(data["ats_score"], int)
    assert "supported_ats" in data


def test_resume_optimize_pdf():
    payload = {
        "resume_text": "Senior Python engineer with FastAPI, Docker, and AWS experience. Delivered APIs and reduced latency.",
        "job_description": "Looking for Python FastAPI engineer with AWS, PostgreSQL, Redis and strong communication.",
        "ats_provider": "greenhouse",
        "output_format": "pdf",
    }
    r = client.post("/api/v1/resume/optimize", json=payload)
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/pdf")
    assert len(r.content) > 500
