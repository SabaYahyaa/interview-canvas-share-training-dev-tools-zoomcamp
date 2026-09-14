from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status, WebSocket
from pydantic import BaseModel


router = APIRouter(prefix="/v1/sessions", tags=["Sessions"])


class SessionCreate(BaseModel):
    title: str
    prompt: str
    duration_minutes: int
    scheduled_at: Optional[str] = None


class Session(BaseModel):
    id: str
    owner_user_id: str
    title: str
    prompt: str
    state: str
    candidate_editing_enabled: bool
    cursors_visible: bool
    duration_minutes: int
    scheduled_at: Optional[str]
    started_at: Optional[str]
    ended_at: Optional[str]
    created_at: str
    updated_at: str


class Participant(BaseModel):
    id: str
    session_id: str
    user_id: str
    display_name: str
    role: str


sessions = {}
participants = {}


@router.post("", response_model=Session, status_code=status.HTTP_201_CREATED)
async def create_session(session_data: SessionCreate):
    session_id = str(uuid4())
    now = datetime.now().isoformat()

    new_session = Session(
        id=session_id,
        owner_user_id="user-123",
        title=session_data.title,
        prompt=session_data.prompt,
        state="draft",
        candidate_editing_enabled=True,
        cursors_visible=True,
        duration_minutes=session_data.duration_minutes,
        scheduled_at=session_data.scheduled_at,
        started_at=None,
        ended_at=None,
        created_at=now,
        updated_at=now,
    )

    sessions[session_id] = new_session

    return new_session


@router.get("/{session_id}", response_model=Session)
async def get_session(session_id: str):
    session = sessions.get(session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    return session


@router.post(
    "/{session_id}/start",
    response_model=Session,
    status_code=status.HTTP_200_OK,
)
async def start_session(session_id: str):
    session = sessions.get(session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    now = datetime.now().isoformat()

    session.state = "live"
    session.started_at = now
    session.updated_at = now

    return session


@router.post(
    "/{session_id}/participants",
    response_model=Participant,
    status_code=status.HTTP_201_CREATED,
)
async def add_participant(session_id: str):
    session = sessions.get(session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    participant = Participant(
        id=str(uuid4()),
        session_id=session_id,
        user_id="user-123",
        display_name="Test User",
        role="interviewer",
    )

    participants[participant.id] = participant

    return participant


@router.websocket("/{session_id}/realtime")
async def realtime(session_id: str, websocket: WebSocket):
    await websocket.accept(subprotocol="sdip")

    if session_id not in sessions:
        await websocket.close(code=1008)
        return

    try:
        while True:
            message = await websocket.receive_json()
            await websocket.send_json(message)
    except Exception:
        await websocket.close()


