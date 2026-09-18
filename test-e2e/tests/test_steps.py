import os
import requests
import pytest

BASE_URL = os.getenv("E2E_BASE_URL", "http://localhost:8000")

def test_health_check():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200

def test_workflow_steps():
    # Update to a valid route registered in sessions.router or guest.router
    response = requests.get(f"{BASE_URL}/v1/sessions")  # Adjust path to match your router
    assert response.status_code in (200, 201)
    data = response.json()
    assert data is not None