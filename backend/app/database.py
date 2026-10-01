import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

INTERVIEWER_USER_ID = os.getenv("INTERVIEWER_USER_ID", "user-123")
INTERVIEWER_EMAIL = os.getenv("INTERVIEWER_EMAIL", "host@example.com")
INTERVIEWER_DISPLAY_NAME = os.getenv("INTERVIEWER_DISPLAY_NAME", "Interviewer")

# Default to SQLite if DATABASE_URL is not set or if testing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Handle Render's postgres:// prefix requirement
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configure sqlite vs postgres engine parameters
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

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
    # Skip database initialization during test execution
    if os.getenv("TESTING") == "1":
        return

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
