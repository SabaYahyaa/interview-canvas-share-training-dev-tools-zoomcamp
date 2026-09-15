import asyncio
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker

# --- DATABASE SETUP (SQLAlchemy + SQLite) ---

# To switch to PostgreSQL later, simply replace this URL with:
# DATABASE_URL = "postgresql://user:password@localhost:5432/dbname"
DATABASE_URL = "sqlite:///./interview.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


# --- SQLALCHEMY DATABASE MODELS ---


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String, nullable=False)
    created_at = Column(String, default=utc_now)


class InterviewSessionModel(Base):
    __tablename__ = "interview_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    owner_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    prompt = Column(Text, default="")
    state = Column(String, default="active")  # draft | live | active | ended | archived
    candidate_editing_enabled = Column(Boolean, default=True)
    cursors_visible = Column(Boolean, default=True)
    duration_minutes = Column(Integer, default=60)
    scheduled_at = Column(String, nullable=True)
    started_at = Column(String, nullable=True)
    ended_at = Column(String, nullable=True)
    created_at = Column(String, default=utc_now)
    updated_at = Column(String, default=utc_now, onupdate=utc_now)

    participants = relationship(
        "ParticipantModel", back_populates="session", cascade="all, delete-orphan"
    )
    canvas = relationship(
        "CanvasDocumentModel",
        back_populates="session",
        uselist=False,
        cascade="all, delete-orphan",
    )


class ParticipantModel(Base):
    __tablename__ = "participants"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    session_id = Column(String, ForeignKey("interview_sessions.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    display_name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # owner | interviewer | candidate | observer
    color = Column(String, default="#3b82f6")
    joined_at = Column(String, default=utc_now)

    session = relationship("InterviewSessionModel", back_populates="participants")


class CanvasDocumentModel(Base):
    __tablename__ = "canvas_documents"

    session_id = Column(
        String, ForeignKey("interview_sessions.id"), primary_key=True
    )
    elements_json = Column(Text, default="[]")  # Stored as JSON string
    version = Column(Integer, default=1)
    updated_at = Column(String, default=utc_now)

    session = relationship("InterviewSessionModel", back_populates="canvas")


class GuestLinkModel(Base):
    __tablename__ = "guest_links"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    session_id = Column(
        String, ForeignKey("interview_sessions.id"), nullable=False
    )
    token = Column(String, unique=True, index=True, nullable=False)
    role_granted = Column(String, default="candidate")
    created_at = Column(String, default=utc_now)


# Create tables on startup
Base.metadata.create_all(bind=engine)


# --- PYDANTIC SCHEMAS ---


class UserSchema(BaseModel):
    id: str
    email: str
    display_name: str
    created_at: str

    class Config:
        from_attributes = True


class ParticipantSchema(BaseModel):
    id: str
    session_id: str
    user_id: Optional[str] = None
    display_name: str
    role: str
    color: str
    joined_at: str

    class Config:
        from_attributes = True


class InterviewSessionSchema(BaseModel):
    id: str
    owner_user_id: str
    title: str
    prompt: str
    state: str
    candidate_editing_enabled: bool
    cursors_visible: bool
    duration_minutes: int
    scheduled_at: Optional[str] = None
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class CanvasDocumentSchema(BaseModel):
    session_id: str
    elements: List[Dict[str, Any]]
    version: int
    updated_at: str


class GuestLinkSchema(BaseModel):
    id: str
    session_id: str
    token: str
    role_granted: str
    created_at: str

    class Config:
        from_attributes = True


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


# --- FASTAPI APP INITIALIZATION ---

app = FastAPI(title="Live Interview Canvas API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Seed Mock User and Default Session
def seed_default_data():
    db = SessionLocal()
    try:
        mock_user = db.query(UserModel).filter_by(id="user-123").first()
        if not mock_user:
            mock_user = UserModel(
                id="user-123",
                email="avery@northwind.dev",
                display_name="Avery Dev",
            )
            db.add(mock_user)

        default_session_id = "0555c12d-19cb-4911-a6c8-20b0ae80b0f8"
        session = db.query(InterviewSessionModel).filter_by(id=default_session_id).first()
        if not session:
            now = utc_now()
            session = InterviewSessionModel(
                id=default_session_id,
                owner_user_id="user-123",
                title="Data Analyst Interview",
                prompt="Create an ETL pipeline diagram",
                state="active",
                started_at=now,
            )
            db.add(session)

            owner = ParticipantModel(
                id="part-123",
                session_id=default_session_id,
                user_id="user-123",
                display_name="Avery Dev",
                role="owner",
            )
            db.add(owner)

            canvas = CanvasDocumentModel(
                session_id=default_session_id,
                elements_json="[]",
                version=1,
            )
            db.add(canvas)

            db.commit()
    finally:
        db.close()


seed_default_data()

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


@app.get("/v1/me", response_model=UserSchema)
async def get_current_user(db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(id="user-123").first()
    return user


@app.get("/v1/sessions")
async def list_sessions(db: Session = Depends(get_db)):
    sessions = db.query(InterviewSessionModel).all()
    result = []
    for s in sessions:
        parts = [ParticipantSchema.model_validate(p) for p in s.participants]
        sess_data = InterviewSessionSchema.model_validate(s).model_dump()
        result.append({**sess_data, "participants": parts, "link": None})
    return result


@app.post("/v1/sessions", response_model=InterviewSessionSchema)
async def create_session(req: CreateSessionRequest, db: Session = Depends(get_db)):
    now = utc_now()
    new_id = str(uuid4())

    session = InterviewSessionModel(
        id=new_id,
        owner_user_id="user-123",
        title=req.title,
        prompt=req.prompt,
        state="active",
        duration_minutes=req.duration_minutes,
        scheduled_at=req.scheduled_at,
        started_at=now,
    )
    db.add(session)

    owner = ParticipantModel(
        id=str(uuid4()),
        session_id=new_id,
        user_id="user-123",
        display_name="Avery Dev",
        role="owner",
    )
    db.add(owner)

    canvas = CanvasDocumentModel(session_id=new_id, elements_json="[]", version=1)
    db.add(canvas)

    db.commit()
    db.refresh(session)
    return session


@app.get("/v1/sessions/{session_id}")
async def get_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(InterviewSessionModel).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    parts = [ParticipantSchema.model_validate(p) for p in session.participants]
    sess_data = InterviewSessionSchema.model_validate(session)
    return {"session": sess_data, "participants": parts, "link": None}


@app.patch("/v1/sessions/{session_id}", response_model=InterviewSessionSchema)
async def update_session(
    session_id: str, patch: UpdateSessionRequest, db: Session = Depends(get_db)
):
    session = db.query(InterviewSessionModel).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    data = patch.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(session, key, value)
    session.updated_at = utc_now()

    db.commit()
    db.refresh(session)

    sess_schema = InterviewSessionSchema.model_validate(session)
    await ws_manager.broadcast(
        session_id,
        {"type": "permission_changed", "sessionId": session_id, "session": sess_schema.model_dump()},
    )
    return session


@app.post("/v1/sessions/{session_id}/start", response_model=InterviewSessionSchema)
async def start_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(InterviewSessionModel).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.state = "active"
    session.started_at = utc_now()
    session.updated_at = utc_now()
    db.commit()
    db.refresh(session)
    return session


@app.post("/v1/sessions/{session_id}/end", response_model=InterviewSessionSchema)
async def end_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(InterviewSessionModel).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.state = "ended"
    session.ended_at = utc_now()
    session.updated_at = utc_now()
    db.commit()
    db.refresh(session)

    await ws_manager.broadcast(session_id, {"type": "session_ended", "sessionId": session_id})
    return session


@app.post("/v1/sessions/{session_id}/participants")
async def join_as_owner(session_id: str, db: Session = Depends(get_db)):
    owner = (
        db.query(ParticipantModel)
        .filter_by(session_id=session_id, role="owner")
        .first()
    )
    if not owner:
        owner = ParticipantModel(
            id=str(uuid4()),
            session_id=session_id,
            user_id="user-123",
            display_name="Avery Dev",
            role="owner",
        )
        db.add(owner)
        db.commit()
        db.refresh(owner)
    return owner


@app.delete("/v1/sessions/{session_id}/participants/{participant_id}")
async def remove_participant(session_id: str, participant_id: str, db: Session = Depends(get_db)):
    part = (
        db.query(ParticipantModel)
        .filter_by(session_id=session_id, id=participant_id)
        .first()
    )
    if part:
        db.delete(part)
        db.commit()
        await ws_manager.broadcast(
            session_id,
            {"type": "presence_leave", "sessionId": session_id, "participantId": participant_id},
        )
    return True


# --- CANVAS ROUTING ---


@app.get("/v1/sessions/{session_id}/canvas", response_model=CanvasDocumentSchema)
async def get_canvas(session_id: str, db: Session = Depends(get_db)):
    canvas = db.query(CanvasDocumentModel).filter_by(session_id=session_id).first()
    if not canvas:
        canvas = CanvasDocumentModel(session_id=session_id, elements_json="[]", version=1)
        db.add(canvas)
        db.commit()
        db.refresh(canvas)

    return CanvasDocumentSchema(
        session_id=canvas.session_id,
        elements=json.loads(canvas.elements_json),
        version=canvas.version,
        updated_at=canvas.updated_at,
    )


@app.put("/v1/sessions/{session_id}/canvas")
async def save_canvas(session_id: str, req: SaveCanvasRequest, db: Session = Depends(get_db)):
    canvas = db.query(CanvasDocumentModel).filter_by(session_id=session_id).first()
    if not canvas:
        canvas = CanvasDocumentModel(session_id=session_id)
        db.add(canvas)

    canvas.elements_json = json.dumps(req.elements)
    canvas.version += 1
    canvas.updated_at = utc_now()
    db.commit()

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


@app.post("/v1/sessions/{session_id}/guest-links", response_model=GuestLinkSchema)
async def create_guest_link(
    session_id: str, payload: dict = None, db: Session = Depends(get_db)
):
    role = payload.get("role_granted", "candidate") if payload else "candidate"
    token = str(uuid4())[:8]

    link = GuestLinkModel(session_id=session_id, token=token, role_granted=role)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@app.get("/v1/join/{token}")
async def inspect_token(token: str, db: Session = Depends(get_db)):
    link = db.query(GuestLinkModel).filter_by(token=token).first()
    if not link:
        raise HTTPException(status_code=404, detail="Invalid token")
    session = db.query(InterviewSessionModel).filter_by(id=link.session_id).first()
    return {"session": session, "link": link, "activeCount": 1}


@app.post("/v1/join/{token}")
async def join_session(token: str, req: JoinRequest, db: Session = Depends(get_db)):
    link = db.query(GuestLinkModel).filter_by(token=token).first()
    if not link:
        raise HTTPException(status_code=404, detail="Invalid token")
    session = db.query(InterviewSessionModel).filter_by(id=link.session_id).first()

    participant = ParticipantModel(
        session_id=link.session_id,
        display_name=req.display_name,
        role=link.role_granted,
    )
    db.add(participant)
    db.commit()
    db.refresh(participant)

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
