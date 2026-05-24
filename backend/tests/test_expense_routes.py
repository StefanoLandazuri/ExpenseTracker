import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.auth.jwt import create_access_token

client = TestClient(app)


@pytest.fixture(autouse=True)
def patch_dynamo(dynamo_table):
    with patch("app.routes.expenses.dynamo.get_table", return_value=dynamo_table), \
        patch("app.routes.auth.dynamo.get_table", return_value=dynamo_table), \
        patch("app.db.dynamo.get_table", return_value=dynamo_table):
        yield


def auth_headers(user_id: str = "user-123") -> dict:
    token = create_access_token(user_id)
    return {"Authorization": f"Bearer {token}"}


EXPENSE_PAYLOAD = {
    "amount": "50.00",
    "category": "food",
    "description": "Groceries",
    "date": "2024-01-15",
}


# --- Auth required ---

def test_create_expense_requires_auth():
    res = client.post("/expenses", json=EXPENSE_PAYLOAD)
    assert res.status_code == 403


# --- Create ---

def test_create_expense_returns_201_with_id():
    res = client.post("/expenses", json=EXPENSE_PAYLOAD, headers=auth_headers())
    assert res.status_code == 201
    data = res.json()
    assert "id" in data
    assert data["category"] == "food"


def test_create_expense_invalid_category_returns_422():
    payload = {**EXPENSE_PAYLOAD, "category": "invalid"}
    res = client.post("/expenses", json=payload, headers=auth_headers())
    assert res.status_code == 422


def test_create_expense_negative_amount_returns_422():
    payload = {**EXPENSE_PAYLOAD, "amount": "-10.00"}
    res = client.post("/expenses", json=payload, headers=auth_headers())
    assert res.status_code == 422


def test_create_expense_with_comma_decimal_is_accepted():
    payload = {**EXPENSE_PAYLOAD, "amount": "50,25"}
    res = client.post("/expenses", json=payload, headers=auth_headers())
    assert res.status_code == 201
    assert res.json()["amount"] == "50.25"


# --- List ---

def test_list_expenses_empty_month_returns_empty_list():
    res = client.get("/expenses?month=2099-01", headers=auth_headers())
    assert res.status_code == 200
    assert res.json()["expenses"] == []


def test_list_expenses_only_returns_own_data():
    # User A crea un gasto
    client.post("/expenses", json=EXPENSE_PAYLOAD, headers=auth_headers("user-A"))

    # User B crea un gasto
    client.post("/expenses", json=EXPENSE_PAYLOAD, headers=auth_headers("user-B"))

    # User A solo ve el suyo
    res = client.get("/expenses?month=2024-01", headers=auth_headers("user-A"))
    expenses = res.json()["expenses"]
    assert len(expenses) == 1
    assert expenses[0]["user_id"] == "user-A"


# --- Delete ---

def test_delete_own_expense_returns_204():
    res_create = client.post("/expenses", json=EXPENSE_PAYLOAD, headers=auth_headers())
    expense_id = res_create.json()["id"]
    date = res_create.json()["date"]

    res = client.delete(f"/expenses/{expense_id}?date={date}", headers=auth_headers())
    assert res.status_code == 204


def test_delete_other_users_expense_returns_404():
    res_create = client.post("/expenses", json=EXPENSE_PAYLOAD, headers=auth_headers("user-owner"))
    expense_id = res_create.json()["id"]
    date = res_create.json()["date"]

    res = client.delete(f"/expenses/{expense_id}?date={date}", headers=auth_headers("user-intruder"))
    assert res.status_code == 404


# --- Summary ---

def test_summary_empty_month_returns_zeros():
    res = client.get("/expenses/summary?month=2099-01", headers=auth_headers())
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == "0"
    assert data["by_category"]["food"] == "0"


def test_summary_calculates_total_correctly():
    client.post("/expenses", json={**EXPENSE_PAYLOAD, "amount": "30.00"}, headers=auth_headers("user-sum"))
    client.post("/expenses", json={**EXPENSE_PAYLOAD, "amount": "20.00"}, headers=auth_headers("user-sum"))

    res = client.get("/expenses/summary?month=2024-01", headers=auth_headers("user-sum"))
    assert res.status_code == 200
    assert float(res.json()["total"]) == 50.0


def test_summary_groups_by_category_correctly():
    client.post("/expenses", json={**EXPENSE_PAYLOAD, "amount": "40.00", "category": "food"}, headers=auth_headers("user-cat"))
    client.post("/expenses", json={**EXPENSE_PAYLOAD, "amount": "60.00", "category": "transport"}, headers=auth_headers("user-cat"))

    res = client.get("/expenses/summary?month=2024-01", headers=auth_headers("user-cat"))
    data = res.json()
    assert float(data["by_category"]["food"]) == 40.0
    assert float(data["by_category"]["transport"]) == 60.0
    assert float(data["by_category"]["housing"]) == 0.0