from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import pytest

from app.auth.passwords import hash_password, verify_password
from app.auth.jwt import create_access_token, create_refresh_token, decode_token
from app.config import settings


# --- Password tests ---

def test_hash_password_returns_different_string():
    plain = "mypassword123"
    hashed = hash_password(plain)
    assert hashed != plain


def test_verify_correct_password_returns_true():
    plain = "mypassword123"
    hashed = hash_password(plain)
    assert verify_password(plain, hashed) is True


def test_verify_wrong_password_returns_false():
    hashed = hash_password("mypassword123")
    assert verify_password("wrongpassword", hashed) is False


# --- JWT tests ---

def test_access_token_decodes_correctly():
    token = create_access_token("user-123")
    payload = decode_token(token)
    assert payload["sub"] == "user-123"
    assert payload["type"] == "access"


def test_expired_token_raises_error():
    expire = datetime.now(timezone.utc) - timedelta(minutes=1)
    payload = {"sub": "user-123", "exp": expire, "type": "access"}
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    with pytest.raises(JWTError):
        decode_token(token)


def test_refresh_token_has_refresh_type_claim():
    token = create_refresh_token("user-123")
    payload = decode_token(token)
    assert payload["type"] == "refresh"