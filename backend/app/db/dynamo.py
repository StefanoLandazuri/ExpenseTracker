import boto3
from boto3.dynamodb.conditions import Key

from app.config import settings


def get_client():
    kwargs = {
        "region_name": settings.aws_region,
        "aws_access_key_id": "local",
        "aws_secret_access_key": "local",
    }
    if settings.dynamodb_endpoint:
        kwargs["endpoint_url"] = settings.dynamodb_endpoint
    return boto3.resource("dynamodb", **kwargs)


def get_table():
    return  get_client().Table(settings.dynamodb_table)


def put_expense(user_id: str, expense: dict) -> None:
    table = get_table()
    table.put_item(Item={
        "PK": f"USER#{user_id}",
        "SK": f"EXPENSE#{expense['date']}#{expense['id']}",
        **expense,
    })


def query_expenses_by_month(user_id: str, month: str) -> list[dict]:
    table = get_table()
    response = table.query(
        KeyConditionExpression=(
            Key("PK").eq(f"USER#{user_id}") &
            Key("SK").begins_with(f"EXPENSE#{month}")
        )
    )
    return response.get("Items", [])


def get_expense(user_id: str, expense_id: str, date: str) -> dict | None:
    table = get_table()
    response = table.get_item(Key={
        "PK": f"USER#{user_id}",
        "SK": f"EXPENSE#{date}#{expense_id}",
    })
    return response.get("Item")


def delete_expense(user_id: str, expense_id: str, date: str) -> bool:
    table = get_table()
    sk = f"EXPENSE#{date}#{expense_id}"
    existing = table.get_item(Key={
        "PK": f"USER#{user_id}",
        "SK": sk,
    }).get("Item")

    if not existing:
        return False

    table.delete_item(Key={
        "PK": f"USER#{user_id}",
        "SK": sk,
    })
    return True