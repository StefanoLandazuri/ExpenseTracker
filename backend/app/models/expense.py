from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, field_validator

Category = Literal[
    "food", "transport", "housing", "health",
    "entertainment", "education", "clothing", "other"
]


class ExpenseCreate(BaseModel):
    amount: Decimal
    category: Category
    description: str | None = None
    date: str  # formato YYYY-MM

    @field_validator("amount", mode="before")
    @classmethod
    def normalize_amount_separator(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip().replace(",", ".")
        return value

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("amount must be greater than 0")
        return value

    @field_validator("description")
    @classmethod
    def description_max_length(cls, description: str | None) -> str | None:
        if description is not None and len(description) > 200:
            raise ValueError("description must be 200 characters or less")
        return description


class Expense(ExpenseCreate):
    id: str
    user_id: str
    created_at: str


class ExpenseSummary(BaseModel):
    total: Decimal
    by_category: dict[Category, Decimal]
    by_day: list[dict]