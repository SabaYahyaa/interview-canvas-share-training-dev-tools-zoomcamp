from fastapi.testclient import TestClient
from uuid import uuid4
from main import app


def test_create_session():
    client = TestClient(app)

    response = client.post(
        "/v1/sessions",
        json={
            "title": "Test Title",
            "prompt": "Test Prompt",
            "duration_minutes": 60,
            "scheduled_at": "2023-01-01T00:00:00",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Title"
    assert data["state"] == "draft"


def test_start_session():
    client = TestClient(app)

    response = client.post(
        "/v1/sessions",
        json={
            "title": "Test Title",
            "prompt": "Test Prompt",
            "duration_minutes": 60,
            "scheduled_at": None,
        },
    )

    assert response.status_code == 201

    session_id = response.json()["id"]

    response = client.post(f"/v1/sessions/{session_id}/start")

    assert response.status_code == 200
    data = response.json()
    assert data["state"] == "live"
    assert data["started_at"] is not None


def test_start_session_unknown_id():
    client = TestClient(app)
    unknown_id = str(uuid4())

    response = client.post(f"/v1/sessions/{unknown_id}/start")

    assert response.status_code == 404
    assert response.json() == {"detail": "Session not found"}