def test_websocket_broadcast(client):
    # 1. Create a session first so the DB contains a valid record
    create_resp = client.post(
        "/v1/sessions",
        json={
            "title": "WebSocket Test Room",
            "prompt": "Test Prompt",
            "duration_minutes": 30,
        },
    )
    assert create_resp.status_code == 200
    session_id = create_resp.json()["id"]

    # 2. Connect client sockets using the valid session_id
    with client.websocket_connect(f"/ws/rooms/{session_id}") as ws1:
        with client.websocket_connect(f"/ws/rooms/{session_id}") as ws2:
            payload = {"type": "cursor_move", "x": 120, "y": 350}
            ws1.send_json(payload)
            received = ws2.receive_json()
            assert received == payload