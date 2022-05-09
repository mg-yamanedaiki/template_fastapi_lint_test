from app.database import Session
from app.models import User


def run(db: Session) -> None:
    db.add(User(name="テストユーザー", email="mg.atd.1107@gmail.com"))
    db.commit()
