from typing import Dict, Optional, Set
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, session_id: str, websocket: WebSocket):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = set()
        self.active_connections[session_id].add(websocket)

    def disconnect(self, session_id: str, websocket: WebSocket):
        if session_id in self.active_connections:
            self.active_connections[session_id].discard(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def broadcast(
        self, session_id: str, message: dict, sender: Optional[WebSocket] = None
    ):
        if session_id in self.active_connections:
            for connection in list(self.active_connections[session_id]):
                if connection != sender:
                    try:
                        await connection.send_json(message)
                    except Exception:
                        pass


ws_manager = ConnectionManager()