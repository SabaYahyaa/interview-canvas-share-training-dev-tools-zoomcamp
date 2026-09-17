import os
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Seed constants
INTERVIEWER_USER_ID = os.getenv("INTERVIEWER_USER_ID", "user-123")
INTERVIEWER_EMAIL = os.getenv("INTERVIEWER_EMAIL", "host@example.com")
INTERVIEWER_DISPLAY_NAME = os.getenv("INTERVIEWER_DISPLAY_NAME", "Interviewer")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/interviewer_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency for obtaining a DB session in FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_db():
    # Import models here to prevent circular import on startup
    from app.models import UserModel

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        user = db.query(UserModel).filter_by(id=INTERVIEWER_USER_ID).first()
        if not user:
            interviewer = UserModel(
                id=INTERVIEWER_USER_ID,
                email=INTERVIEWER_EMAIL,
                display_name=INTERVIEWER_DISPLAY_NAME,
            )
            db.add(interviewer)
            db.commit()
            print(f"Seeded default interviewer: {INTERVIEWER_DISPLAY_NAME}")
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")
        raise
    finally:
        db.close()
