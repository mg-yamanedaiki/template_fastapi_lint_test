from calendar import monthrange
from datetime import datetime


class YearRange:
    start: datetime
    finish: datetime

    def __init__(self, year: int) -> None:
        self.start = datetime(year=year, month=1, day=1)
        self.finish = datetime(
            year=year,
            month=12,
            day=monthrange(year, 12)[1],
        )


def get_year_range(year: int) -> YearRange:
    return YearRange(year=year)
