import os
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./interview.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_db():
    # Import models inside function or at top level to ensure tables are registered
    from app.models import UserModel

    # Create all database tables if they don't exist yet
    Base.metadata.create_all(bind=engine)

    # Seed default host user required by routes
    db = SessionLocal()
    try:
        user = db.query(UserModel).filter_by(id="user-123").first()
        if not user:
            db.add(
                UserModel(id="user-123", name="Interviewer", email="host@example.com")
            )
            db.commit()
    finally:
        db.close()