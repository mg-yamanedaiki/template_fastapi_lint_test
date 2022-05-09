from datetime import date, timedelta
from typing import Generator


def date_range(
    start: date,
    stop: date,
    step: timedelta = timedelta(1),
) -> Generator[date, None, None]:
    current = start
    while current < stop:
        yield current
        current += step
