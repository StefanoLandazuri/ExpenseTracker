import pytest
from decimal import Decimal
from unittest.mock import patch

from app.db import dynamo


USER_ID = "user-123"

EXPENSE_1 = {
    "id": "exp-1",
    "date": "2024-01",
    "amount": Decimal("50.00"),
    "category": "food",
    "description": "Groceries",
}
EXPENSE_2 = {
    "id": "exp-2",
    "date": "2024-01",
    "amount": Decimal("20.00"),
    "category": "transport",
    "description": "Bus",
}
EXPENSE_3 = {
    "id": "exp-3",
    "date": "2024-02",
    "amount": Decimal("100.00"),
    "category": "housing",
    "description": "Rent",
}


@pytest.fixture(autouse=True)
def patch_table(dynamo_table):
    with patch("app.db.dynamo.get_table", return_value=dynamo_table):
        yield


def test_put_and_query_expense():
    dynamo.put_expense(USER_ID, EXPENSE_1)
    results = dynamo.query_expenses_by_month(USER_ID, "2024-01")
    assert len(results) == 1
    assert results[0]["id"] == "exp-1"


def test_query_empty_month_returns_empty_list():
    results = dynamo.query_expenses_by_month(USER_ID, "2024-03")
    assert results == []


def test_delete_existing_expense_returns_true():
    dynamo.put_expense(USER_ID, EXPENSE_1)
    result = dynamo.delete_expense(USER_ID, "exp-1", "2024-01")
    assert result is True


def test_delete_nonexistent_expense_returns_false():
    result = dynamo.delete_expense(USER_ID, "no-existe", "2024-01")
    assert result is False


def test_query_filters_by_month_correctly():
    dynamo.put_expense(USER_ID, EXPENSE_1)
    dynamo.put_expense(USER_ID, EXPENSE_2)
    dynamo.put_expense(USER_ID, EXPENSE_3)

    results_jan = dynamo.query_expenses_by_month(USER_ID, "2024-01")
    results_feb = dynamo.query_expenses_by_month(USER_ID, "2024-02")

    assert len(results_jan) == 2
    assert len(results_feb) == 1
    assert results_feb[0]["id"] == "exp-3"