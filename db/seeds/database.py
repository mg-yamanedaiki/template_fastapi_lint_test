from app.database import SessionLocal

from . import user


def run() -> None:
    try:
        db = SessionLocal()
        user.run(db)
    finally:
        db.close()
