from datetime import datetime

from pydantic import BaseModel, Field


class TimeStamp(BaseModel):
    created_at: datetime = Field(title="作成日")
    updated_at: datetime = Field(title="更新日")
