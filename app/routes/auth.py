from datetime import datetime

from cognito_pyauth.exceptions import (
    NotAuthorizedException,
    UsernameExistsException,
    UserNotConfirmedException,
)
from cognito_pyauth.schemas import RefreshTokenResult
from fastapi import APIRouter, Depends, status

from app.auth import auth, get_current_user
from app.constants import HTTPExceptionType
from app.database import Session, get_db
from app.exceptions import HTTPException
from app.models import User
from app.schemas import (
    AuthResponse,
    ConfirmSignupRequest,
    LoginRequest,
    RefreshTokenRequest,
    RefreshTokenResponse,
    ResendConfirmationCodeRequest,
    SignupRequest,
    UserResponse,
)

router = APIRouter()


@router.post(
    "/login",
    summary="ログイン",
    response_model=AuthResponse,
    response_description="ログインユーザー情報",
)
def login(req: LoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    try:
        res = auth.login(req.email, req.password.get_secret_value())
    except UserNotConfirmedException:
        error_msg = "このメールアドレスは検証されていません"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="このメールアドレスは検証されていません",
            type_=HTTPExceptionType.NOT_CONFIRMED,
        )
    except NotAuthorizedException:
        error_msg = "メールアドレスもしくはパスワードが間違えています"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_msg,
            type_=HTTPExceptionType.UN_AUTHORIZED,
        )
    user = db.query(User).filter(User.email == req.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="このユーザーはデータベースに登録されていません",
        )
    return AuthResponse(**res.dict(), user=UserResponse.from_orm(user))


@router.get(
    "/whoami",
    summary="ログイン中ユーザーを返却",
    response_model=UserResponse,
    response_description="ログイン中ユーザー",
)
def whoami(
    user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse.from_orm(user)


@router.post(
    "/signup",
    summary="サインアップ",
    response_model=UserResponse,
    response_description="サインアップユーザー情報",
)
def signup(req: SignupRequest, db: Session = Depends(get_db)) -> UserResponse:
    try:
        auth.signup(req.email, req.password.get_secret_value())
    except UsernameExistsException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="このメールアドレスはすでに使用されています",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

    user = User(
        email=req.email,
        name="",
        remark="",
    )
    db.add(user)
    db.commit()

    return UserResponse.from_orm(user)


@router.post(
    "/confirmSignup",
    summary="サインアップの検証",
    response_model=UserResponse,
    response_description="サインアップユーザー情報",
)
def confirm_signup(req: ConfirmSignupRequest) -> UserResponse:
    try:
        test = auth.confirm_signup(req.email, req.confirmation_code)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

    print(test)
    return UserResponse(
        id=1,
        email=req.email,
        name="",
        remark="",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@router.post(
    "/resendConfirmationCode",
    summary="検証コードの再送信",
)
def resend_confirmation_code(req: ResendConfirmationCodeRequest) -> None:
    try:
        auth.resend_confirmation_code(req.email)
    except Exception as e:
        print(e)


@router.post(
    "/refreshToken",
    summary="トークンの更新",
    response_model=RefreshTokenResponse,
    response_description="更新済みトークン",
)
def refresh_token(req: RefreshTokenRequest) -> RefreshTokenResult:
    try:
        return auth.refresh_token(req.refresh_token)
    except Exception as e:
        print(e)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="更新トークンの期限が切れています",
    )
