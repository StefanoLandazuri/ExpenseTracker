from datetime import datetime, timezone
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Query,Response
import csv
import io
from ulid import ULID

from app.auth.dependencies import get_current_user
from app.db import dynamo
from app.errors import NotFound
from app.models.expense import Category, Expense, ExpenseCreate, ExpenseSummary

router = APIRouter(prefix="/expenses", tags=["expenses"])


def _to_expense(item: dict) -> Expense:
    return Expense(
        id=item["id"],
        user_id=item["user_id"],
        amount=item["amount"],
        category=item["category"],
        description=item.get("description"),
        date=item["date"],
        created_at=item["created_at"],
    )


def calculate_summary(expenses: list[Expense], month: str) -> ExpenseSummary:
    from calendar import monthrange

    year, mon = map(int, month.split("-"))
    _, days_in_month = monthrange(year, mon)

    total = Decimal("0")
    by_category: dict[Category, Decimal] = {
        "food": Decimal("0"),
        "transport": Decimal("0"),
        "housing": Decimal("0"),
        "health": Decimal("0"),
        "entertainment": Decimal("0"),
        "education": Decimal("0"),
        "clothing": Decimal("0"),
        "other": Decimal("0"),
    }
    by_day_map: dict[str, Decimal] = {}

    for exp in expenses:
        total += exp.amount
        by_category[exp.category] += exp.amount
        day_key = exp.date
        by_day_map[day_key] = by_day_map.get(day_key, Decimal("0")) + exp.amount

    by_day = [
        {
            "date": f"{month}-{str(d).zfill(2)}",
            "total": by_day_map.get(f"{month}-{str(d).zfill(2)}", Decimal("0")),
        }
        for d in range(1, days_in_month + 1)
    ]

    return ExpenseSummary(total=total, by_category=by_category, by_day=by_day)


@router.post("", status_code=201)
def create_expense(
    body: ExpenseCreate,
    user_id: Annotated[str, Depends(get_current_user)],
) -> dict:
    expense_id = str(ULID())
    now = datetime.now(timezone.utc).isoformat()
    expense = Expense(
        id=expense_id,
        user_id=user_id,
        amount=body.amount,
        category=body.category,
        description=body.description,
        date=body.date,
        created_at=now,
    )
    dynamo.put_expense(user_id, expense.model_dump())
    return expense.model_dump()


@router.get("")
def list_expenses(
    user_id: Annotated[str, Depends(get_current_user)],
    month: str = Query(default=datetime.now(timezone.utc).strftime("%Y-%m")),
) -> dict:
    items = dynamo.query_expenses_by_month(user_id, month)
    expenses = [_to_expense(item) for item in items]
    return {"expenses": [e.model_dump() for e in expenses]}


@router.delete("/{expense_id}", status_code=204)
def delete_expense(
    expense_id: str,
    user_id: Annotated[str, Depends(get_current_user)],
    date: str = Query(),
) -> None:
    deleted = dynamo.delete_expense(user_id, expense_id, date)
    if not deleted:
        raise NotFound()


@router.get("/summary")
def get_summary(
    user_id: Annotated[str, Depends(get_current_user)],
    month: str = Query(default=datetime.now(timezone.utc).strftime("%Y-%m")),
) -> dict:
    items = dynamo.query_expenses_by_month(user_id, month)
    expenses = [_to_expense(item) for item in items]
    summary = calculate_summary(expenses, month)
    return summary.model_dump()

@router.get("/export")
def export_expenses(
    user_id: Annotated[str, Depends(get_current_user)],
    month: str = Query(default=datetime.now(timezone.utc).strftime("%Y-%m")),
) -> Response:
    items = dynamo.query_expenses_by_month(user_id, month)
    expenses = [_to_expense(item) for item in items]

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["date", "category", "amount", "description"])
    for exp in sorted(expenses, key=lambda e: e.date):
        writer.writerow([exp.date, exp.category, exp.amount, exp.description or ""])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="expenses-{month}.csv"'
        },
    )