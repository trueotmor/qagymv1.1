from enum import IntEnum

class HTTPStatus(IntEnum):
    
    # Успешные (2xx)
    OK = 200
    CREATED = 201
    # ACCEPTED = 202
    NO_CONTENT = 204
    
    # Клиентские ошибки (4xx)
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    # CONFLICT = 409
    # UNPROCESSABLE_ENTITY = 422
    
    # Серверные ошибки (5xx)
    INTERNAL_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503