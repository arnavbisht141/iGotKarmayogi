import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

db_url = settings.DATABASE_URL

# Normalize Supabase / standard PostgreSQL connection strings for psycopg2
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

connect_args = {}
engine_kwargs = {"echo": False}

if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    # If a path is specified with a subfolder (e.g., /app/data/karmayogi.db), ensure folder exists
    raw_path = db_url.split("sqlite:///")[-1].split("sqlite://")[-1]
    if raw_path and not raw_path.startswith(":memory:"):
        parent_dir = os.path.dirname(raw_path)
        if parent_dir and not os.path.exists(parent_dir):
            try:
                os.makedirs(parent_dir, exist_ok=True)
            except Exception:
                pass
else:
    # Production connection pool settings for PostgreSQL / Supabase.
    # Opening a connection to hosted Postgres costs 1-2 s, so connections are kept warm and long-lived
    # instead of being recycled every few minutes; TCP keepalives stop idle ones from being dropped.
    engine_kwargs.update({
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20,
        "pool_recycle": 1800,
        "pool_use_lifo": True,  # reuse the most recently used (still warm) connection first
    })
    connect_args = {
        "connect_timeout": 30,  # generous: a slow link should delay startup, not crash it
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }

engine = create_engine(
    db_url,
    connect_args=connect_args,
    **engine_kwargs
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def warm_connection_pool(connections: int = 4) -> None:
    """Opens pooled connections up front so the first page loads do not each pay the connection cost."""
    if db_url.startswith("sqlite"):
        return
    from concurrent.futures import ThreadPoolExecutor
    from sqlalchemy import text

    def _open(_):
        with engine.connect() as conn:
            conn.execute(text("select 1"))

    with ThreadPoolExecutor(max_workers=connections) as pool:
        list(pool.map(_open, range(connections)))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
