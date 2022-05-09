from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin(object):
    @declared_attr
    def created_at(cls) -> Column:
        return Column(
            DateTime,
            default=datetime.now,
            nullable=False,
            comment="作成日時",
        )

    @declared_attr
    def updated_at(cls) -> Column:
        return Column(
            DateTime,
            default=datetime.now,
            onupdate=datetime.now,
            nullable=False,
            comment="更新日時",
        )
