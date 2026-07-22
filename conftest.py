"""Общие фикстуры.

'page', 'context' и 'browser' приходят из pytest-playwright и здесь не
переопределяются. Всё ниже — надстройка page object'ов и тестовых данных.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import Page

from config import Credentials, get_base_url, get_credentials
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.secure_page import SecurePage


@pytest.fixture(scope="session")
def base_url(request: pytest.FixtureRequest) -> str:
    """Окружение под тест.

    Приоритет: опция CLI '--base-url' > переменная 'BASE_URL' > значение по умолчанию.
    pytest-playwright подхватывает эту фикстуру и задаёт её в контексте браузера,
    поэтому работает и относительная навигация.
    """
    from_cli = request.config.getoption("--base-url")
    return (from_cli or get_base_url()).rstrip("/")


@pytest.fixture(scope="session")
def credentials() -> Credentials:
    return get_credentials()


@pytest.fixture
def main_page(page: Page, base_url: str) -> MainPage:
    """Главная страница, уже открытая."""
    return MainPage(page, base_url).open()


@pytest.fixture
def login_page(page: Page, base_url: str) -> LoginPage:
    """Страница входа, уже открытая."""
    return LoginPage(page, base_url).open()


@pytest.fixture
def secure_page(
    login_page: LoginPage,
    page: Page,
    base_url: str,
    credentials: Credentials,
) -> SecurePage:
    """Аутентифицированная сессия на защищённой странице.

    Используется тестами, которым нужен залогиненный пользователь, но которые
    сами не проверяют сценарий входа.
    """
    login_page.login(credentials.username, credentials.password)
    return SecurePage(page, base_url)
