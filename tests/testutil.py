from logging import getLogger

from app import models
from app.database import SessionLocal

logger = getLogger(__name__)


def create_test_user() -> models.User:
    db = SessionLocal()
    user = models.User(email="mg.atd.1107@gmail.com")
    db.add(user)
    db.close()
    return user
