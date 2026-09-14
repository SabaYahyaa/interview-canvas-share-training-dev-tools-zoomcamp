import uuid
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from backend.auth.security import verify_access_token
from backend.models.schemas import User, Role, InterviewSession, Participant, TokenData
from backend.store.inmemory import (
    get_user_by_id,
    get_session_by_id,
    get_guest_link_by_token,
    get_participants_for_session,
    participants_db
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    token_data = verify_access_token(token, credentials_exception)
    user_id = UUID(token_data.username) # Assuming username in token is user_id
    user = get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user

def get_current_participant(session_id: UUID, token: str = Depends(oauth2_scheme)) -> Participant:
    # Try to authenticate as a regular user first (owner or invited participant)
    try:
        user = get_current_user(token)
        # Check if the user is an owner of the session
        session = get_session_by_id(session_id)
        if session and session.owner_id == user.id:
            # Find or create an owner participant for the session
            owner_participant = next((p for p in get_participants_for_session(session_id) if p.user_id == user.id and p.role.__root__ == "owner"), None)
            if owner_participant:
                return owner_participant
            else:
                # Create owner participant if not exists (e.g., if only owner_id was set)
                new_owner_participant = Participant(
                    id=uuid.uuid4(),
                    session_id=session_id,
                    user_id=user.id,
                    display_name=user.display_name, # Use user's display name
                    role=Role(__root__="owner"),
                    joined_at=datetime.now(timezone.utc),
                    last_seen_at=datetime.now(timezone.utc),
                    is_present=True,
                )
                participants_db[new_owner_participant.id] = new_owner_participant
                return new_owner_participant
        
        # Check if the user is an explicitly added participant (non-owner)
        participants = [p for p in get_participants_for_session(session_id) if p.user_id == user.id]
        if participants:
            return participants[0]

    except HTTPException: # This means the token might be a guest token or invalid
        pass

    # If not a regular user or owner, try to authenticate as a guest
    guest_link = get_guest_link_by_token(token)
    if guest_link and guest_link.session_id == session_id:
        # Check if there's an existing participant for this guest link and session
        # For simplicity, assuming guest participants don't have user_ids and are uniquely identified by role and session for this flow
        # A more robust solution might tie guest participants to the guest link ID or a temporary guest ID.
        existing_guest_participant = next((
            p for p in get_participants_for_session(session_id)
            if p.user_id is None and p.role.__root__ == guest_link.role_granted.__root__
        ), None)
        
        if existing_guest_participant:
            return existing_guest_participant
        
        # If no existing guest participant for this link/session/role, create one
        session = get_session_by_id(session_id)
        if session:
            guest_participant = Participant(
                id=uuid.uuid4(),
                session_id=session_id,
                user_id=None, # Guest participants do not have a registered user_id
                display_name=f"Guest {guest_link.role_granted.__root__.capitalize()}", # Generic display name for initial guest join
                role=Role(__root__=guest_link.role_granted.__root__),
                joined_at=datetime.now(timezone.utc),
                last_seen_at=datetime.now(timezone.utc),
                is_present=True,
            )
            participants_db[guest_participant.id] = guest_participant
            return guest_participant

    raise credentials_exception

