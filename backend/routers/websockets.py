from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

@router.websocket("/v1/sessions/{session_id}/realtime")
async def websocket_realtime_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        while True:
            # Keep the connection open and respond to ping/messages
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        print(f"Client disconnected from realtime session: {session_id}")