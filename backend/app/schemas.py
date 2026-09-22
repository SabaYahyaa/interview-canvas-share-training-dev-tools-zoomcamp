from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: str
    email: str
    display_name: str

    model_config = ConfigDict(from_attributes=True)


class ParticipantSchema(BaseModel):
    id: str
    session_id: str
    user_id: Optional[str] = None
    display_name: str
    role: str
    color: str
    joined_at: str

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


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
