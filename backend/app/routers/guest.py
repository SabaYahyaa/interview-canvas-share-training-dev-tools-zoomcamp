from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GuestLinkModel, InterviewSessionModel, ParticipantModel
from app.schemas import GuestLinkSchema, JoinRequest
from app.websockets import ws_manager

router = APIRouter(tags=["Guest Links & WebSockets"])


@router.post("/v1/sessions/{session_id}/guest-links", response_model=GuestLinkSchema)
async def create_guest_link(
    session_id: str, payload: dict = None, db: Session = Depends(get_db)
):
    # Validate session existence
    session = db.query(InterviewSessionModel).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    role = payload.get("role_granted", "candidate") if payload else "candidate"
    token = str(uuid4())[:8]

    link = GuestLinkModel(session_id=session_id, token=token, role_granted=role)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@router.get("/v1/join/{token}")
async def inspect_token(token: str, db: Session = Depends(get_db)):
    link = db.query(GuestLinkModel).filter_by(token=token).first()
    if not link:
        raise HTTPException(status_code=404, detail="Invalid token")
    session = db.query(InterviewSessionModel).filter_by(id=link.session_id).first()
    return {"session": session, "link": link, "activeCount": 1}


@router.post("/v1/join/{token}")
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

    # Return session_id explicitly at the root level so the frontend can read data.session_id or data.session.id
    return {
        "participant": participant,
        "session": session,
        "session_id": link.session_id,
    }


@router.websocket("/ws/rooms/{session_id}")
async def room_websocket(websocket: WebSocket, session_id: str):
    await ws_manager.connect(session_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await ws_manager.broadcast(session_id, data, sender=websocket)
    except WebSocketDisconnect:
        ws_manager.disconnect(session_id, websocket)
