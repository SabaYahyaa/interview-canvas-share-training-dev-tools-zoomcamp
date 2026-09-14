import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
from uuid import uuid4

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Live Interview Canvas API")

# Enable CORS for local Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- IN-MEMORY DATA MODELS ---

class User(BaseModel):
    id: str
    email: str
    display_name: str
    created_at: str

class Participant(BaseModel):
    id: str
    session_id: str
    user_id: Optional[str] = None
    display_name: str
    role: str  # "owner" | "interviewer" | "candidate" | "observer"
    color: str = "#3b82f6"
    joined_at: str

class InterviewSession(BaseModel):
    id: str
    owner_user_id: str
    title: str
    prompt: str
    state: str  # "draft" | "live" | "active" | "ended" | "archived"
    candidate_editing_enabled: bool = True
    cursors_visible: bool = True
    duration_minutes: int = 60
    scheduled_at: Optional[str] = None
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    created_at: str
    updated_at: str

class CanvasDocument(BaseModel):
    session_id: str
    elements: List[Dict[str, Any]] = Field(default_factory=list)
    version: int = 1
    updated_at: str

class GuestLink(BaseModel):
    id: str
    session_id: str
    token: str
    role_granted: str = "candidate"
    created_at: str

# Request DTOs
class CreateSessionRequest(BaseModel):
    title: str
    prompt: str = ""
    duration_minutes: int = 60
    scheduled_at: Optional[str] = None

class UpdateSessionRequest(BaseModel):
    title: Optional[str] = None
    prompt: Optional[str] = None
    candidate_editing_enabled: Optional[bool] = None
    cursors_visible: Optional[bool] = None
    state: Optional[str] = None

class SaveCanvasRequest(BaseModel):
    elements: List[Dict[str, Any]]
    actor: str

class JoinRequest(BaseModel):
    display_name: str

# --- IN-MEMORY DATABASE STORAGE ---

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

MOCK_USER = User(
    id="user-123",
    email="avery@northwind.dev",
    display_name="Avery Dev",
    created_at=utc_now(),
)

# Storage dictionary containers
db_sessions: Dict[str, InterviewSession] = {}
db_participants: Dict[str, List[Participant]] = {}  # session_id -> list
db_canvases: Dict[str, CanvasDocument] = {}         # session_id -> doc
db_guest_links: Dict[str, GuestLink] = {}          # token -> link

# Seed default session for easy testing
default_session_id = "0555c12d-19cb-4911-a6c8-20b0ae80b0f8"
db_sessions[default_session_id] = InterviewSession(
    id=default_session_id,
    owner_user_id=MOCK_USER.id,
    title="Data Analyst Interview",
    prompt="Create an ETL pipeline diagram",
    state="active",
    candidate_editing_enabled=True,
    cursors_visible=True,
    duration_minutes=60,
    started_at=utc_now(),
    created_at=utc_now(),
    updated_at=utc_now(),
)

db_participants[default_session_id] = [
    Participant(
        id="part-123",
        session_id=default_session_id,
        user_id=MOCK_USER.id,
        display_name=MOCK_USER.display_name,
        role="owner",
        joined_at=utc_now(),
    )
]

db_canvases[default_session_id] = CanvasDocument(
    session_id=default_session_id,
    elements=[],
    version=1,
    updated_at=utc_now(),
)

# --- WEBSOCKET CONNECTION MANAGER ---

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

    async def broadcast(self, session_id: str, message: dict, sender: Optional[WebSocket] = None):
        if session_id in self.active_connections:
            for connection in list(self.active_connections[session_id]):
                if connection != sender:
                    try:
                        await connection.send_json(message)
                    except Exception:
                        pass

ws_manager = ConnectionManager()

# --- REST ENDPOINTS ---

@app.get("/v1/me", response_model=User)
async def get_current_user():
    return MOCK_USER

@app.get("/v1/sessions")
async def list_sessions():
    result = []
    for s_id, sess in db_sessions.items():
        parts = db_participants.get(s_id, [])
        result.append({
            **sess.model_dump(),
            "participants": parts,
            "link": None
        })
    return result

@app.post("/v1/sessions", response_model=InterviewSession)
async def create_session(req: CreateSessionRequest):
    new_id = str(uuid4())
    now = utc_now()
    session = InterviewSession(
        id=new_id,
        owner_user_id=MOCK_USER.id,
        title=req.title,
        prompt=req.prompt,
        state="active",
        duration_minutes=req.duration_minutes,
        scheduled_at=req.scheduled_at,
        started_at=now,
        created_at=now,
        updated_at=now,
    )
    db_sessions[new_id] = session
    db_participants[new_id] = [
        Participant(
            id=str(uuid4()),
            session_id=new_id,
            user_id=MOCK_USER.id,
            display_name=MOCK_USER.display_name,
            role="owner",
            joined_at=now,
        )
    ]
    db_canvases[new_id] = CanvasDocument(
        session_id=new_id, elements=[], version=1, updated_at=now
    )
    return session

@app.get("/v1/sessions/{session_id}")
async def get_session(session_id: str):
    session = db_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    parts = db_participants.get(session_id, [])
    return {"session": session, "participants": parts, "link": None}

@app.patch("/v1/sessions/{session_id}", response_model=InterviewSession)
async def update_session(session_id: str, patch: UpdateSessionRequest):
    session = db_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    data = patch.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(session, key, value)
    session.updated_at = utc_now()

    await ws_manager.broadcast(
        session_id,
        {"type": "permission_changed", "sessionId": session_id, "session": session.model_dump()},
    )
    return session

@app.post("/v1/sessions/{session_id}/start", response_model=InterviewSession)
async def start_session(session_id: str):
    session = db_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.state = "active"
    session.started_at = utc_now()
    session.updated_at = utc_now()
    return session

@app.post("/v1/sessions/{session_id}/end", response_model=InterviewSession)
async def end_session(session_id: str):
    session = db_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.state = "ended"
    session.ended_at = utc_now()
    session.updated_at = utc_now()

    await ws_manager.broadcast(
        session_id, {"type": "session_ended", "sessionId": session_id}
    )
    return session

@app.post("/v1/sessions/{session_id}/participants")
async def join_as_owner(session_id: str):
    parts = db_participants.get(session_id, [])
    owner = next((p for p in parts if p.role == "owner"), None)
    if not owner:
        owner = Participant(
            id=str(uuid4()),
            session_id=session_id,
            user_id=MOCK_USER.id,
            display_name=MOCK_USER.display_name,
            role="owner",
            joined_at=utc_now(),
        )
        parts.append(owner)
        db_participants[session_id] = parts
    return owner

@app.delete("/v1/sessions/{session_id}/participants/{participant_id}")
async def remove_participant(session_id: str, participant_id: str):
    if session_id in db_participants:
        db_participants[session_id] = [
            p for p in db_participants[session_id] if p.id != participant_id
        ]
        await ws_manager.broadcast(
            session_id,
            {"type": "presence_leave", "sessionId": session_id, "participantId": participant_id},
        )
    return True

# --- CANVAS ROUTING ---

@app.get("/v1/sessions/{session_id}/canvas", response_model=CanvasDocument)
async def get_canvas(session_id: str):
    canvas = db_canvases.get(session_id)
    if not canvas:
        canvas = CanvasDocument(session_id=session_id, elements=[], version=1, updated_at=utc_now())
        db_canvases[session_id] = canvas
    return canvas

@app.put("/v1/sessions/{session_id}/canvas")
async def save_canvas(session_id: str, req: SaveCanvasRequest):
    canvas = db_canvases.get(session_id)
    if not canvas:
        canvas = CanvasDocument(session_id=session_id, elements=[], version=1, updated_at=utc_now())
    
    canvas.elements = req.elements
    canvas.version += 1
    canvas.updated_at = utc_now()
    db_canvases[session_id] = canvas

    await ws_manager.broadcast(
        session_id,
        {
            "type": "document_update",
            "sessionId": session_id,
            "elements": req.elements,
            "actor": req.actor,
        },
    )
    return "saved"

# --- GUEST ACCESS ---

@app.post("/v1/sessions/{session_id}/guest-links", response_model=GuestLink)
async def create_guest_link(session_id: str, payload: dict = None):
    role = payload.get("role_granted", "candidate") if payload else "candidate"
    token = str(uuid4())[:8]
    link = GuestLink(
        id=str(uuid4()),
        session_id=session_id,
        token=token,
        role_granted=role,
        created_at=utc_now(),
    )
    db_guest_links[token] = link
    return link

@app.get("/v1/join/{token}")
async def inspect_token(token: str):
    link = db_guest_links.get(token)
    if not link:
        raise HTTPException(status_code=404, detail="Invalid token")
    session = db_sessions.get(link.session_id)
    return {"session": session, "link": link, "activeCount": 1}

@app.post("/v1/join/{token}")
async def join_session(token: str, req: JoinRequest):
    link = db_guest_links.get(token)
    if not link:
        raise HTTPException(status_code=404, detail="Invalid token")
    session = db_sessions.get(link.session_id)
    
    participant = Participant(
        id=str(uuid4()),
        session_id=link.session_id,
        user_id=None,
        display_name=req.display_name,
        role=link.role_granted,
        joined_at=utc_now(),
    )
    db_participants.setdefault(link.session_id, []).append(participant)
    return {"participant": participant, "session": session}

@app.get("/v1/sessions/{session_id}/audit")
async def get_audit(session_id: str):
    return []

# --- WEBSOCKET ENDPOINT ---

@app.websocket("/ws/rooms/{session_id}")
async def room_websocket(websocket: WebSocket, session_id: str):
    await ws_manager.connect(session_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await ws_manager.broadcast(session_id, data, sender=websocket)
    except WebSocketDisconnect:
        ws_manager.disconnect(session_id, websocket)