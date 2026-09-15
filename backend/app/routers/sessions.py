import json
from typing import Any, Dict, List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db, utc_now
from app.models import (
    CanvasDocumentModel,
    InterviewSessionModel,
    ParticipantModel,
    UserModel,
)
from app.schemas import (
    CanvasDocumentSchema,
    CreateSessionRequest,
    InterviewSessionSchema,
    ParticipantSchema,
    SaveCanvasRequest,
    UpdateSessionRequest,
    UserSchema,
)
from app.websockets import ws_manager

router = APIRouter(prefix="/v1", tags=["Sessions & Canvas"])


@router.get("/me", response_model=UserSchema)
async def get_current_user(db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(id="user-123").first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, # 404
            detail="User not found",
        )
    return user


@router.get("/sessions", response_model=List[Dict[str, Any]])
async def list_sessions(db: Session = Depends(get_db)):
    sessions = db.query(InterviewSessionModel).all()
    result = []
    for s in sessions:
        parts = [ParticipantSchema.model_validate(p) for p in s.participants]
        sess_data = InterviewSessionSchema.model_validate(s).model_dump()
        result.append({**sess_data, "participants": parts, "link": None})
    return result


@router.post("/sessions", response_model=InterviewSessionSchema)
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


@router.get("/sessions/{session_id}")
async def get_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(InterviewSessionModel).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    parts = [ParticipantSchema.model_validate(p) for p in session.participants]
    sess_data = InterviewSessionSchema.model_validate(session)
    return {"session": sess_data, "participants": parts, "link": None}


@router.patch("/sessions/{session_id}", response_model=InterviewSessionSchema)
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
        {
            "type": "permission_changed",
            "sessionId": session_id,
            "session": sess_schema.model_dump(),
        },
    )
    return session


@router.post("/sessions/{session_id}/start", response_model=InterviewSessionSchema)
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


@router.post("/sessions/{session_id}/end", response_model=InterviewSessionSchema)
async def end_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(InterviewSessionModel).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.state = "ended"
    session.ended_at = utc_now()
    session.updated_at = utc_now()
    db.commit()
    db.refresh(session)

    await ws_manager.broadcast(
        session_id, {"type": "session_ended", "sessionId": session_id}
    )
    return session


@router.post("/sessions/{session_id}/participants")
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


@router.delete("/sessions/{session_id}/participants/{participant_id}")
async def remove_participant(
    session_id: str, participant_id: str, db: Session = Depends(get_db)
):
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
            {
                "type": "presence_leave",
                "sessionId": session_id,
                "participantId": participant_id,
            },
        )
    return True


@router.get("/sessions/{session_id}/canvas", response_model=CanvasDocumentSchema)
async def get_canvas(session_id: str, db: Session = Depends(get_db)):
    canvas = db.query(CanvasDocumentModel).filter_by(session_id=session_id).first()
    if not canvas:
        canvas = CanvasDocumentModel(
            session_id=session_id, elements_json="[]", version=1
        )
        db.add(canvas)
        db.commit()
        db.refresh(canvas)

    return CanvasDocumentSchema(
        session_id=canvas.session_id,
        elements=json.loads(canvas.elements_json),
        version=canvas.version,
        updated_at=canvas.updated_at,
    )


@router.put("/sessions/{session_id}/canvas")
async def save_canvas(
    session_id: str, req: SaveCanvasRequest, db: Session = Depends(get_db)
):
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


@router.get("/sessions/{session_id}/audit")
async def get_audit(session_id: str):
    return []