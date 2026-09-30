import os

from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()
"""Временное решение через dataclass, в реальной разработке использовать переменные окружения"""
@dataclass(frozen=True)
class Settings:
    database_url: str
    cors_origins: list[str]


def get_settings() -> Settings:
    return Settings(
        database_url=(
            f"postgresql+psycopg://"
            f"{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}"
        ),
        cors_origins=os.environ["CORS_ORIGINS"].split(","),
    )

