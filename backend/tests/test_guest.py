import pytest


def test_invalid_token_inspection(client):
    response = client.get("/v1/join/invalid-token-123")
    assert response.status_code == 404
    assert response.json()["detail"] in ["Invalid token", "API route not found"]


def test_websocket_broadcast_in_room(client):
    session_id = "test-ws-room-888"

    with client.websocket_connect(f"/ws/rooms/{session_id}") as ws1:
        with client.websocket_connect(f"/ws/rooms/{session_id}") as ws2:
            payload = {"type": "code_update", "code": "def hello(): pass"}
            ws1.send_json(payload)
            received = ws2.receive_json()
            assert received == payload