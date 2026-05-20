from datetime import timedelta
from fastapi import APIRouter, Cookie, Response
from jose import JWTError

from app.auth.jwt import create_access_token, create_refresh_token, decode_token
from app.auth.passwords import hash_password, verify_password
from app.db import dynamo
from app.errors import EmailAlreadyExists, InvalidCredentials, TokenExpired
from app.models.user import User, UserCreate
from app.config import settings
import uuid
from datetime import datetime, timezone

router = APIRouter(prefix="/auth", tags=["auth"])

REFRESH_MAX_AGE = settings.refresh_token_days * 24 * 60 * 60


def _set_refresh_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        secure=False,  # True en prod
        samesite="lax",
        path="/auth/refresh",
        max_age=REFRESH_MAX_AGE,
    )


@router.post("/register", status_code=201)
def register(body: UserCreate, response: Response) -> dict:
    existing = dynamo.get_user_by_email(body.email)
    if existing:
        raise EmailAlreadyExists()

    user_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    user_in_db = {
        "id": user_id,
        "email": body.email,
        "password_hash": hash_password(body.password),
        "created_at": now,
    }
    dynamo.put_user(user_in_db)

    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    _set_refresh_cookie(response, refresh_token)

    user = User(id=user_id, email=body.email, created_at=now)
    return {"user": user.model_dump(), "access_token": access_token}


@router.post("/login")
def login(body: UserCreate, response: Response) -> dict:
    user_in_db = dynamo.get_user_by_email(body.email)
    if not user_in_db:
        raise InvalidCredentials()

    if not verify_password(body.password, user_in_db["password_hash"]):
        raise InvalidCredentials()

    access_token = create_access_token(user_in_db["id"])
    refresh_token = create_refresh_token(user_in_db["id"])
    _set_refresh_cookie(response, refresh_token)

    user = User(
        id=user_in_db["id"],
        email=user_in_db["email"],
        created_at=user_in_db["created_at"],
    )
    return {"user": user.model_dump(), "access_token": access_token}


@router.post("/refresh")
def refresh(response: Response, refresh_token: str | None = Cookie(default=None)) -> dict:
    if not refresh_token:
        raise TokenExpired()

    try:
        payload = decode_token(refresh_token)
    except JWTError:
        raise TokenExpired()

    if payload.get("type") != "refresh":
        raise TokenExpired()

    user_id = payload["sub"]
    new_access_token = create_access_token(user_id)
    new_refresh_token = create_refresh_token(user_id)
    _set_refresh_cookie(response, new_refresh_token)

    return {"access_token": new_access_token}