from pydantic import BaseModel, Field, PositiveInt

from .timestamp import TimeStamp


class UserBase(BaseModel):
    email: str = Field(title="メールアドレス")
    remark: str = Field(default="", title="備考")


class UserResponse(UserBase, TimeStamp):
    id: PositiveInt = Field(title="ユーザーID")

    class Config:
        orm_mode = True
