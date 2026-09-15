import pytest
from app.models import UserModel

def test_get_current_user(client):
    response = client.get("/v1/me")
    assert response.status_code == 200
    assert response.json()["id"] == "user-123"


def test_create_session(client):
    payload = {
        "title": "System Architecture Review",
        "prompt": "Design a distributed queueing system",
        "duration_minutes": 60,
    }
    response = client.post("/v1/sessions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data


def test_get_session_not_found(client):
    response = client.get("/v1/sessions/invalid-uuid-123")
    assert response.status_code == 404