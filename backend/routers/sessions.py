from datetime import datetime
from typing import Any, Dict, List, Optional
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SessionResponse(BaseModel):
    id: str
    owner_user_id: str
    title: str
    prompt: str
    state: str
    candidate_editing_enabled: bool = True
    cursors_visible: bool = True
    duration_minutes: int = 60
    scheduled_at: Optional[str] = None
    started_at: Optional[str] = None
    ended_at: Optional[str] = None

class ParticipantResponse(BaseModel):
    id: str
    session_id: str
    user_id: str
    role: str

# --- SESSION ENDPOINTS ---

@router.get("/v1/sessions", response_model=List[SessionResponse])
async def list_sessions():
    return [
        {
            "id": "0555c12d-19cb-4911-a6c8-20b0ae80b0f8",
            "owner_user_id": "user-123",
            "title": "data analyst",
            "prompt": "create ETL",
            "state": "active",
            "candidate_editing_enabled": True,
            "cursors_visible": True,
            "duration_minutes": 60,
            "scheduled_at": None,
            "started_at": None,
            "ended_at": None,
        }
    ]

@router.post("/v1/sessions", response_model=SessionResponse)
async def create_session(payload: Dict[str, Any]):
    return {
        "id": "0555c12d-19cb-4911-a6c8-20b0ae80b0f8",
        "owner_user_id": "user-123",
        "title": payload.get("title", "data analyst"),
        "prompt": payload.get("prompt", "create ETL"),
        "state": "draft",
        "candidate_editing_enabled": True,
        "cursors_visible": True,
        "duration_minutes": payload.get("duration_minutes", 60),
        "scheduled_at": None,
        "started_at": None,
        "ended_at": None,
    }

@router.get("/v1/sessions/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    return {
        "id": session_id,
        "owner_user_id": "user-123",
        "title": "data analyst",
        "prompt": "create ETL",
        "state": "active",
        "candidate_editing_enabled": True,
        "cursors_visible": True,
        "duration_minutes": 60,
        "scheduled_at": None,
        "started_at": None,
        "ended_at": None,
    }

@router.post("/v1/sessions/{session_id}/start", response_model=SessionResponse)
async def start_session(session_id: str):
    return {
        "id": session_id,
        "owner_user_id": "user-123",
        "title": "data analyst",
        "prompt": "create ETL",
        "state": "active",
        "candidate_editing_enabled": True,
        "cursors_visible": True,
        "duration_minutes": 60,
        "scheduled_at": None,
        "started_at": datetime.utcnow().isoformat(),
        "ended_at": None,
    }

# --- CANVAS & PARTICIPANT ENDPOINTS ---

@router.get("/v1/sessions/{session_id}/canvas")
async def get_session_canvas(session_id: str):
    return {
        "session_id": session_id,
        "nodes": [],
        "edges": [],
        "viewport": {"x": 0, "y": 0, "zoom": 1},
    }

@router.get("/v1/sessions/{session_id}/participants", response_model=List[ParticipantResponse])
async def get_participants(session_id: str):
    return [
        {
            "id": "part-123",
            "session_id": session_id,
            "user_id": "user-123",
            "role": "interviewer",
        }
    ]

@router.post("/v1/sessions/{session_id}/participants", response_model=ParticipantResponse)
async def add_participant(session_id: str, payload: Dict[str, Any] = {}):
    return {
        "id": "part-123",
        "session_id": session_id,
        "user_id": "user-123",
        "role": payload.get("role", "interviewer"),
    }

@router.get("/v1/sessions/{session_id}/snapshots")
async def get_session_snapshots(session_id: str):
    return [
        {
            "id": "snap-123",
            "session_id": session_id,
            "data": {},
            "created_at": datetime.utcnow().isoformat(),
        }
    ]

@router.post("/v1/sessions/{session_id}/tokens")
async def create_session_token(session_id: str, payload: Dict[str, Any] = {}):
    return {
        "token": "mock-room-token-123",
        "session_id": session_id,
        "user_id": "user-123",
        "role": "interviewer",
    }