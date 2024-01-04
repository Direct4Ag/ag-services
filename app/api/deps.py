from typing import Generator

from app.core.config import get_settings
from app.db.session import SessionLocal

settings = get_settings()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
