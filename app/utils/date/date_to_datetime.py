from datetime import date, datetime, time
from typing import Optional


def date_to_datetime(date_: Optional[date]) -> Optional[datetime]:
    if date_ is None:
        return None
    return datetime.combine(date_, time())
