from typing import Optional

from fastapi import status
from pydantic import BaseModel, EmailStr, Field, SecretStr, validator

from app.constants import HTTPExceptionType
from cognito_pyauth.schemas import RefreshTokenResult

from .user import UserResponse


class UnAuthorizedErrorResponse(BaseModel):
    status_code: int = Field(
        default=status.HTTP_401_UNAUTHORIZED,
        title="ステータスコード",
        const=True,
    )
    detail: str = Field(default="", title="詳細")
    type: Optional[HTTPExceptionType] = Field(default=None, title="エラータイプ")


class SignupRequest(BaseModel):
    email: EmailStr = Field(title="メールアドレス")
    password: SecretStr = Field(title="パスワード", min_length=8, max_length=24)


class LoginRequest(BaseModel):
    email: EmailStr = Field(title="メールアドレス")
    password: SecretStr = Field(title="パスワード", min_length=8, max_length=24)


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(title="更新トークン")


class ConfirmSignupRequest(BaseModel):
    email: EmailStr = Field(title="メールアドレス")
    confirmation_code: str = Field(title="検証コード")

    @validator("confirmation_code")
    def confirmation_code_validator(cls, v: str) -> str:
        if not v.isnumeric() or len(v) != 6:
            raise ValueError("検証コードは6桁の数字です")
        return v


class ResendConfirmationCodeRequest(BaseModel):
    email: EmailStr = Field(title="メールアドレス")


class TokenResponse(BaseModel):
    access_token: str = Field(title="アクセストークン")
    id_token: str = Field(title="IDトークン")
    refresh_token: str = Field(title="更新トークン")
    expires_in: int = Field(title="有効期限(秒)")


class AuthResponse(TokenResponse):
    user: UserResponse = Field(title="ユーザー")


class RefreshTokenResponse(RefreshTokenResult):
    pass
