from .utils import StrEnum


class HTTPExceptionType(StrEnum):
    NOT_CONFIRMED = "not_confirmed"
    UN_AUTHORIZED = "un_authorized"
    VALIDATION_ERROR = "validation_error"
