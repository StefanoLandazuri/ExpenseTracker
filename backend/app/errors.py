from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int):
        self.code = code
        self.message = message
        self.status_code = status_code


class EmailAlreadyExists(AppError):
    def __init__(self):
        super().__init__("EMAIL_ALREADY_EXISTS", "Email already registered", 409)


class InvalidCredentials(AppError):
    def __init__(self):
        super().__init__("INVALID_CREDENTIALS", "Invalid email or password", 401)


class TokenExpired(AppError):
    def __init__(self):
        super().__init__("TOKEN_EXPIRED", "Token has expired", 401)


class NotFound(AppError):
    def __init__(self):
        super().__init__("NOT_FOUND", "Resource not found", 404)


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )