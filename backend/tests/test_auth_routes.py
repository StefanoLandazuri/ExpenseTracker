import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def patch_dynamo(dynamo_table):
    with patch("app.routes.auth.dynamo.get_table", return_value=dynamo_table), \
         patch("app.db.dynamo.get_table", return_value=dynamo_table):
        yield


# --- Register ---

def test_register_creates_user_and_returns_token():
    res = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "12345678"
    })
    assert res.status_code == 201
    data = res.json()
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"


def test_register_duplicate_email_returns_409():
    client.post("/auth/register", json={
        "email": "dup@example.com",
        "password": "12345678"
    })
    res = client.post("/auth/register", json={
        "email": "dup@example.com",
        "password": "12345678"
    })
    assert res.status_code == 409
    assert res.json()["error"]["code"] == "EMAIL_ALREADY_EXISTS"


def test_register_invalid_email_returns_422():
    res = client.post("/auth/register", json={
        "email": "not-an-email",
        "password": "12345678"
    })
    assert res.status_code == 422


def test_register_short_password_returns_422():
    res = client.post("/auth/register", json={
        "email": "short@example.com",
        "password": "123"
    })
    assert res.status_code == 422


# --- Login ---

def test_login_with_correct_credentials_returns_token():
    client.post("/auth/register", json={
        "email": "login@example.com",
        "password": "12345678"
    })
    res = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "12345678"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_with_wrong_password_returns_401():
    client.post("/auth/register", json={
        "email": "wrong@example.com",
        "password": "12345678"
    })
    res = client.post("/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrongpassword"
    })
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "INVALID_CREDENTIALS"


def test_login_with_nonexistent_email_returns_401():
    res = client.post("/auth/login", json={
        "email": "noexiste@example.com",
        "password": "12345678"
    })
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "INVALID_CREDENTIALS"


# --- Refresh ---

def test_refresh_with_valid_cookie_returns_new_token():
    res_register = client.post("/auth/register", json={
        "email": "refresh@example.com",
        "password": "12345678"
    })
    assert res_register.status_code == 201

    # refresh_token cookie is set by the register endpoint, so we can just call refresh without manually setting it
    res = client.post("/auth/refresh")
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_refresh_without_cookie_returns_401():
    # New client without cookies
    from fastapi.testclient import TestClient as FreshClient
    fresh = FreshClient(app)
    res = fresh.post("/auth/refresh")
    assert res.status_code == 401


def test_refresh_with_access_token_in_cookie_returns_401():
    from app.auth.jwt import create_access_token
    from fastapi.testclient import TestClient as FreshClient
    fresh = FreshClient(app)
    fresh.cookies.set("refresh_token", create_access_token("user-123"), path="/auth/refresh")
    res = fresh.post("/auth/refresh")
    assert res.status_code == 401