from datetime import datetime
from typing import List, Literal, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

# --- Core Entities from frontend/src/lib/api/types.ts ---

class User(BaseModel):
    id: UUID
    email: str
    display_name: str
    avatar_url: Optional[str] = None
    hashed_password: str # Added for backend User model

class Role(BaseModel):
    __root__: Literal["owner", "interviewer", "candidate"]

class GuestRole(BaseModel):
    __root__: Literal["interviewer", "candidate"]

class CanvasElement(BaseModel):
    id: str
    type: str
    x: float
    y: float
    width: float
    height: float
    text: Optional[str] = None
    color: Optional[str] = None
    # Add other properties as needed based on frontend usage

class CanvasDocument(BaseModel):
    elements: List[CanvasElement]

class Cursor(BaseModel):
    x: float
    y: float

class Participant(BaseModel):
    id: UUID
    session_id: UUID
    user_id: Optional[UUID] = None
    display_name: str
    role: Role
    joined_at: datetime
    last_seen_at: datetime
    is_present: bool = True
    # Frontend also has 'cursor' on Participant for presence updates, but it's often null.
    # We'll handle cursor updates as separate WebSocket messages.

class GuestLink(BaseModel):
    id: UUID
    session_id: UUID
    role_granted: GuestRole
    created_at: datetime
    expires_at: Optional[datetime] = None
    token: str

class InterviewSession(BaseModel):
    id: UUID
    owner_id: UUID
    title: str
    prompt: str
    created_at: datetime
    updated_at: datetime
    scheduled_at: Optional[datetime] = None
    duration_minutes: int
    status: Literal["draft", "scheduled", "live", "ended", "archived"]

class SessionListItem(InterviewSession):
    participants: List[Participant] = []
    link: Optional[GuestLink] = None

class SessionDetail(BaseModel):
    session: InterviewSession
    participants: List[Participant]
    link: Optional[GuestLink] = None

class AuditEvent(BaseModel):
    id: UUID
    session_id: UUID
    event: str
    at: datetime
    actor: str

# --- Authentication Models ---

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    user: User

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []

# --- Session Models ---

class CreateSessionRequest(BaseModel):
    title: str
    prompt: str
    duration_minutes: int
    scheduled_at: Optional[datetime] = None

class UpdateSessionPatch(BaseModel):
    title: Optional[str] = None
    prompt: Optional[str] = None
    duration_minutes: Optional[int] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[Literal["draft", "scheduled", "live", "ended", "archived"]] = None

# --- Guest Access Models ---

class CreateGuestLinkRequest(BaseModel):
    role_granted: GuestRole = Field(default="candidate")

class TokenInspection(BaseModel):
    session: InterviewSession
    link: GuestLink
    activeCount: int = 0

class JoinRequest(BaseModel):
    display_name: str

class JoinResponse(BaseModel):
    participant: Participant
    session: InterviewSession

# --- Canvas Models ---

class SaveCanvasRequest(BaseModel):
    elements: List[CanvasElement]
    actor: str

# --- WebSocket / Real-time Communication Models (RoomMessage from frontend/src/lib/api/api.ts) ---

class DocumentUpdateMessage(BaseModel):
    type: Literal["document_update"] = "document_update"
    sessionId: UUID
    elements: List[CanvasElement]
    actor: str

class PresenceUpdateMessage(BaseModel):
    type: Literal["presence_update"] = "presence_update"
    sessionId: UUID
    participant: Participant
    cursor: Optional[Cursor] = None

class PresenceLeaveMessage(BaseModel):
    type: Literal["presence_leave"] = "presence_leave"
    sessionId: UUID
    participantId: UUID

class PermissionChangedMessage(BaseModel):
    type: Literal["permission_changed"] = "permission_changed"
    sessionId: UUID
    session: InterviewSession

class SessionEndedMessage(BaseModel):
    type: Literal["session_ended"] = "session_ended"
    sessionId: UUID

RoomMessage = Union[
    DocumentUpdateMessage,
    PresenceUpdateMessage,
    PresenceLeaveMessage,
    PermissionChangedMessage,
    SessionEndedMessage,
]

# --- Error Models ---

class ApiErrorBody(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None

