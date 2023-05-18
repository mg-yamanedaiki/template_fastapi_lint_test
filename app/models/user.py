from sqlalchemy import Boolean, Column, Integer, String, Text

from app.database import Base
from app.models.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = {"comment": "ユーザー"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=True, comment="顧客ID")
    is_admin = Column(Boolean, default=False, comment="管理者か")
    name = Column(String(50), nullable=False, comment="名前")
    email = Column(String(50), nullable=False, comment="メールアドレス")
    remark = Column(Text, nullable=False, default="", comment="備考")
