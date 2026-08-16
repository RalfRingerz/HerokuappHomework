"""Общие фикстуры.

'page', 'context' и 'browser' приходят из pytest-playwright и здесь не
переопределяются. Всё ниже - это надстройка page object'ов и тестовых данных
"""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from config import Credentials, get_base_url, get_credentials
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.secure_page import SecurePage
from pages.hovers_page import HoversPage
from pages.dynamic_controls_page import DynamicControlsPage


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> None:
    """Маркер critical -> Allure severity CRITICAL (без дублирующих декораторов)"""
    if item.get_closest_marker("critical"):
        allure.dynamic.severity(allure.severity_level.CRITICAL)
        allure.dynamic.tag("critical")


def _page_from_item(item: pytest.Item) -> Page | None:
    """Возвращает Page: из фикстуры page, иначе из page object теста"""
    page = item.funcargs.get("page")
    if isinstance(page, Page):
        return page
    for name in ("main_page", "login_page", "secure_page"):
        page_object = item.funcargs.get(name)
        if page_object is not None and hasattr(page_object, "page"):
            return page_object.page
    return None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """При падении critical теста кладём скриншот в Allure"""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    if not item.get_closest_marker("critical"):
        return
    page = _page_from_item(item)
    if page is None:
        return
    allure.attach(
        page.screenshot(full_page=True),
        name="failure-screenshot",
        attachment_type=allure.attachment_type.PNG,
    )


@pytest.fixture(scope="session")
def base_url(request: pytest.FixtureRequest) -> str:
    """Окружение под тест
    Приоритет: опция CLI '--base-url' > переменная 'BASE_URL' > значение по умолчанию.
    pytest-playwright подхватывает эту фикстуру и задаёт её в контексте браузера,
    поэтому работает и относительная навигация
    """
    from_cli = request.config.getoption("--base-url")
    return (from_cli or get_base_url()).rstrip("/")


@pytest.fixture(scope="session")
def credentials() -> Credentials:
    return get_credentials()


@pytest.fixture
def main_page(page: Page, base_url: str) -> MainPage:
    """Главная страница, уже открытая"""
    return MainPage(page, base_url).open()


@pytest.fixture
def login_page(page: Page, base_url: str) -> LoginPage:
    """Страница входа, уже открытая"""
    return LoginPage(page, base_url).open()


@pytest.fixture
def secure_page(
    login_page: LoginPage,
    page: Page,
    base_url: str,
    credentials: Credentials,
) -> SecurePage:
    """Аутентифицированная сессия на защищённой странице
    Используется тестами, которым нужен залогиненный пользователь, но которые
    сами не проверяют сценарий входа
    """
    login_page.login(credentials.username, credentials.password)
    return SecurePage(page, base_url)


@pytest.fixture
def hovers_page(page: Page, base_url: str) -> HoversPage:
    """Страница с ховерами"""
    return HoversPage(page, base_url).open()


@pytest.fixture
def dynamic_controls_page(page: Page, base_url: str) -> DynamicControlsPage:
    """Страница с динамическими кнопками"""
    return DynamicControlsPage(page, base_url).open()
