from fastapi import Depends, HTTPException, status

from app.database import SessionLocal
from app.models import User
from cognito_pyauth.schemas import Payload

from .auth import auth


def get_current_user(
    payload: Payload = Depends(auth.get_payload_depends),
) -> User:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == payload.email).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="このユーザーは登録されていません",
            )
        return user
    finally:
        db.close()
