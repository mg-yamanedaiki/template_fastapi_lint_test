from typing import Optional

from fastapi import HTTPException as FastAPIHTTPException

from app.constants import HTTPExceptionType


class HTTPException(FastAPIHTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        type_: Optional[HTTPExceptionType] = None,
    ):
        self.status_code = status_code
        self.detail = detail
        self.type_ = type_ if type_ is None else type_.value
