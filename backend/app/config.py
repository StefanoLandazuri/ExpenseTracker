from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    dynamodb_endpoint: str | None = None
    dynamodb_table: str = "expenses"
    aws_region: str = "us-east-1"
    jwt_secret: str = "changeme"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 15
    refresh_token_days: int = 7

    class Config:
        env_file = ".env"


settings = Settings()