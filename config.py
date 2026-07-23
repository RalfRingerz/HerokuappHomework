"""Конфигурация на время прогонов тестов

Каждое значение можно переопределить переменной окружения, чтобы один и тот же
набор тестов можно было запускать против любого деплоя приложения:

    BASE_URL=https://staging.example.com pytest

Опция CLI '--base-url' (из pytest-base-url) имеет приоритет над переменной окружения,
подробнее в 'conftest.py'
"""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_BASE_URL = "https://the-internet.herokuapp.com"


@dataclass(frozen=True)
class Credentials:
    username: str
    password: str


def get_base_url() -> str:
    """Base URL окружения под тест без завершающего слэша"""
    return os.getenv("BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def get_credentials() -> Credentials:
    """Валидные учётные данные для окружения под тест

    По умолчанию это публичные демо-креды. В реальном проекте значений по умолчанию
    не было бы, они приходили бы из хранилища секретов
    """
    return Credentials(
        username=os.getenv("APP_USERNAME", "tomsmith"),
        password=os.getenv("APP_PASSWORD", "SuperSecretPassword!"),
    )
