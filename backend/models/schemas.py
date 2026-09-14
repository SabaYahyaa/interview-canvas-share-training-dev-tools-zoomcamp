from datetime import datetime, timezone
from typing import List, Literal, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


# --- Base Model for Automatic CamelCase Serialization ---

class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        serialize_by_alias=True,
    )


# --- Core Entities ---

class User(CamelModel):
    id: UUID
    email: str
    display_name: str
    avatar_url: Optional[str] = None
    hashed_password: str


class Role(BaseModel):
    __root__: Literal["owner", "interviewer", "candidate"]


class GuestRole(BaseModel):
    __root__: Literal["interviewer", "candidate"]


class CanvasElement(CamelModel):
    id: str
    type: str
    x: float
    y: float
    width: float
    height: float
    text: Optional[str] = None
    color: Optional[str] = None


class CanvasDocument(CamelModel):
    elements: List[CanvasElement] = []


class Cursor(CamelModel):
    x: float
    y: float


class Participant(CamelModel):
    id: UUID
    session_id: UUID
    user_id: Optional[UUID] = None
    display_name: str
    role: Literal["owner", "interviewer", "candidate"]
    joined_at: datetime
    last_seen_at: datetime
    is_present: bool = True


class GuestLink(CamelModel):
    id: UUID
    session_id: UUID
    role_granted: Literal["interviewer", "candidate"]
    created_at: datetime
    expires_at: Optional[datetime] = None
    token: str


class InterviewSession(CamelModel):
    id: UUID
    owner_id: UUID
    title: str
    prompt: str
    created_at: datetime
    updated_at: datetime
    scheduled_at: Optional[datetime] = None
    duration_minutes: int = 0
    status: Literal["draft", "scheduled", "live", "ended", "archived"] = "draft"

    # Time fields required by frontend reportAllChanges & room timer
    start_time: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), alias="startTime"
    )
    started_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), alias="startedAt"
    )


class SessionListItem(InterviewSession):
    participants: List[Participant] = []
    link: Optional[GuestLink] = None


class SessionDetail(CamelModel):
    session: InterviewSession
    participants: List[Participant] = []
    link: Optional[GuestLink] = None


class AuditEvent(CamelModel):
    id: UUID
    session_id: UUID
    event: str
    at: datetime
    actor: str


# --- Authentication Models ---

class LoginRequest(CamelModel):
    email: str
    password: str


class TokenResponse(CamelModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    user: User


class TokenData(CamelModel):
    username: Optional[str] = None
    scopes: List[str] = []


# --- Session Models ---

class CreateSessionRequest(CamelModel):
    title: str
    prompt: str
    duration_minutes: int = 0
    scheduled_at: Optional[datetime] = None


class UpdateSessionPatch(CamelModel):
    title: Optional[str] = None
    prompt: Optional[str] = None
    duration_minutes: Optional[int] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[Literal["draft", "scheduled", "live", "ended", "archived"]] = None


# --- Guest Access Models ---

class CreateGuestLinkRequest(CamelModel):
    role_granted: Literal["interviewer", "candidate"] = "candidate"


class TokenInspection(CamelModel):
    session: InterviewSession
    link: GuestLink
    active_count: int = Field(default=0, alias="activeCount")


class JoinRequest(CamelModel):
    display_name: str


class JoinResponse(CamelModel):
    participant: Participant
    session: InterviewSession


# --- Canvas Models ---

class SaveCanvasRequest(CamelModel):
    elements: List[CanvasElement] = []
    actor: str


# --- WebSocket / Real-time Communication Models ---

class DocumentUpdateMessage(CamelModel):
    type: Literal["document_update"] = "document_update"
    session_id: UUID = Field(alias="sessionId")
    elements: List[CanvasElement] = []
    actor: str


class PresenceUpdateMessage(CamelModel):
    type: Literal["presence_update"] = "presence_update"
    session_id: UUID = Field(alias="sessionId")
    participant: Participant
    cursor: Optional[Cursor] = None


class PresenceLeaveMessage(CamelModel):
    type: Literal["presence_leave"] = "presence_leave"
    session_id: UUID = Field(alias="sessionId")
    participant_id: UUID = Field(alias="participantId")


class PermissionChangedMessage(CamelModel):
    type: Literal["permission_changed"] = "permission_changed"
    session_id: UUID = Field(alias="sessionId")
    session: InterviewSession


class SessionEndedMessage(CamelModel):
    type: Literal["session_ended"] = "session_ended"
    session_id: UUID = Field(alias="sessionId")


RoomMessage = Union[
    DocumentUpdateMessage,
    PresenceUpdateMessage,
    PresenceLeaveMessage,
    PermissionChangedMessage,
    SessionEndedMessage,
]


# --- Error Models ---

class ApiErrorBody(CamelModel):
    code: Optional[str] = None
    message: Optional[str] = None