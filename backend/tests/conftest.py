from typing import Any
import boto3
import pytest
from botocore.exceptions import ClientError

ENDPOINT = "http://localhost:8001"
TABLE_NAME = "expenses"
REGION = "us-east-1"


def make_client():
    return boto3.client(
        "dynamodb",
        endpoint_url=ENDPOINT,
        region_name=REGION,
        aws_access_key_id="local",
        aws_secret_access_key="local",
    )


def create_expenses_table(client):
    client.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {"AttributeName": "PK", "KeyType": "HASH"},
            {"AttributeName": "SK", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"},
            {"AttributeName": "email", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "email-index",
                "KeySchema": [
                    {"AttributeName": "email", "KeyType": "HASH"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            }
        ],
        BillingMode="PAY_PER_REQUEST",
    )


@pytest.fixture
def dynamo_table():
    client = make_client()

    # Borrar si existe de una corrida anterior
    try:
        client.delete_table(TableName=TABLE_NAME)
        client.get_waiter("table_not_exists").wait(TableName=TABLE_NAME)
    except ClientError as e:
        if e.response["Error"]["Code"] != "ResourceNotFoundException":
            raise

    create_expenses_table(client)

    resource = boto3.resource(
        "dynamodb",
        endpoint_url=ENDPOINT,
        region_name=REGION,
        aws_access_key_id="local",
        aws_secret_access_key="local",
    )
    table:Any = resource.Table(TABLE_NAME) # type: ignore

    yield table

    client.delete_table(TableName=TABLE_NAME)