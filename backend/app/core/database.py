import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# For SQLite, check_same_thread needs to be False and ensure parent directory exists
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    # If a path is specified with a subfolder (e.g., /app/data/karmayogi.db), ensure folder exists
    raw_path = settings.DATABASE_URL.split("sqlite:///")[-1].split("sqlite://")[-1]
    if raw_path and not raw_path.startswith(":memory:"):
        parent_dir = os.path.dirname(raw_path)
        if parent_dir and not os.path.exists(parent_dir):
            try:
                os.makedirs(parent_dir, exist_ok=True)
            except Exception:
                pass

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
