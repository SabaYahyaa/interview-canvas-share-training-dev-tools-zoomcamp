def test_websocket_broadcast(client):
    session_id = "test-ws-session-100"
    with client.websocket_connect(f"/ws/rooms/{session_id}") as ws1:
        with client.websocket_connect(f"/ws/rooms/{session_id}") as ws2:
            payload = {"type": "cursor_move", "x": 120, "y": 350}
            ws1.send_json(payload)
            received = ws2.receive_json()
            assert received == payload