from uuid import uuid4
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base, utc_now


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
    state = Column(String, default="active")
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
    role = Column(String, nullable=False)
    color = Column(String, default="#3b82f6")
    joined_at = Column(String, default=utc_now)

    session = relationship("InterviewSessionModel", back_populates="participants")


class CanvasDocumentModel(Base):
    __tablename__ = "canvas_documents"

    session_id = Column(
        String, ForeignKey("interview_sessions.id"), primary_key=True
    )
    elements_json = Column(Text, default="[]")
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