from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)

def test_login_success():
    response = client.post(
        "/v1/auth/login",
        json={"email": "test@example.com", "password": "password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["display_name"] == "Test User"
    # We don't assert created_at directly as it's generated dynamically, but we expect it to be present

def test_login_failure_invalid_credentials():
    response = client.post(
        "/v1/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

def test_login_failure_missing_fields():
    response = client.post(
        "/v1/auth/login",
        json={"email": "test@example.com"} # Missing password
    )
    assert response.status_code == 422 # Unprocessable Entity for Pydantic validation error

    response = client.post(
        "/v1/auth/login",
        json={"password": "password"} # Missing email
    )
    assert response.status_code == 422

