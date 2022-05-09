from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DateTimeFilter(BaseModel):
    started_at: datetime = Field(title="検索開始日")
    finished_at: datetime = Field(title="検索終了日")


class DateTimeOptionalFilter(BaseModel):
    started_at: Optional[datetime] = Field(default=None, title="検索開始日")
    finished_at: Optional[datetime] = Field(default=None, title="検索終了日")
