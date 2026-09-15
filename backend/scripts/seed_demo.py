"""Load the demo dataset into the database configured by DATABASE_URL.

Usage (from backend/):
    python scripts/seed_demo.py              # full seed with LLM quizzes and Pinecone indexing
    python scripts/seed_demo.py --offline    # no LLM or Pinecone calls
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, SessionLocal, engine  # noqa: E402
from app.core.seed_demo import DEMO_EMAIL_DOMAIN, DEMO_PASSWORD, seed_demo  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--offline", action="store_true", help="skip LLM quiz generation and Pinecone indexing")
    args = parser.parse_args()

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        summary = seed_demo(db, use_llm=not args.offline, index_vectors=not args.offline, log=print)
    finally:
        db.close()
    print("Done:", summary)
    print(f"Demo officials sign in as <first>.<last>@{DEMO_EMAIL_DOMAIN} with password {DEMO_PASSWORD}")


if __name__ == "__main__":
    main()
