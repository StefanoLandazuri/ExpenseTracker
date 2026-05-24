import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

from app.config import settings


TABLE_SCHEMA = {
    "TableName": settings.dynamodb_table,
    "KeySchema": [
        {"AttributeName": "PK", "KeyType": "HASH"},
        {"AttributeName": "SK", "KeyType": "RANGE"},
    ],
    "AttributeDefinitions": [
        {"AttributeName": "PK", "AttributeType": "S"},
        {"AttributeName": "SK", "AttributeType": "S"},
        {"AttributeName": "email", "AttributeType": "S"},
    ],
    "GlobalSecondaryIndexes": [
        {
            "IndexName": "email-index",
            "KeySchema": [
                {"AttributeName": "email", "KeyType": "HASH"},
            ],
            "Projection": {"ProjectionType": "ALL"},
        }
    ],
    "BillingMode": "PAY_PER_REQUEST",
}


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
    return  get_client().Table(settings.dynamodb_table) # type: ignore


def ensure_table_exists() -> None:
    if not settings.dynamodb_endpoint:
        return

    client = get_client().meta.client # type: ignore

    try:
        client.describe_table(TableName=settings.dynamodb_table)
        return
    except ClientError as error:
        if error.response["Error"]["Code"] != "ResourceNotFoundException":
            raise

    try:
        client.create_table(**TABLE_SCHEMA)
    except ClientError as error:
        if error.response["Error"]["Code"] != "ResourceInUseException":
            raise


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

def put_user(user:dict) -> None:
    table = get_table()
    table.put_item(Item={
        "PK": f"USER#{user['id']}",
        "SK": "PROFILE",
        "email": user["email"],
        **user,
    })
def get_user_by_email(email: str) -> dict | None:
    table = get_table()
    response = table.query(
        IndexName="email-index",
        KeyConditionExpression=Key("email").eq(email)
    )
    items = response.get("Items", [])
    return items[0] if items else None


def get_user_by_id(user_id: str) -> dict | None:
    table = get_table()
    response = table.get_item(Key={
        "PK": f"USER#{user_id}",
        "SK": "PROFILE",
    })
    return response.get("Item")
