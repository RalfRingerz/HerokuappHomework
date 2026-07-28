"""Сценарий 3 — вход, проверка защищённой области, выход"""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from config import Credentials
from pages.login_page import LoginPage
from pages.secure_page import SecurePage

pytestmark = [
    pytest.mark.ui,
    pytest.mark.e2e,
    pytest.mark.regression,
    pytest.mark.login,
    pytest.mark.auth,
    pytest.mark.positive,
]

EXPECTED_TITLE = "The Internet"
LOGIN_SUCCESS_MESSAGE = "You logged into a secure area!"
LOGOUT_SUCCESS_MESSAGE = "You logged out of the secure area!"
MUST_LOGIN_MESSAGE = "You must login to view the secure area!"
SESSION_COOKIE_NAME = "rack.session"


def _session_cookie(page: Page) -> dict | None:
    """HttpOnly-сессия приложения, в document.cookie её нет"""
    for cookie in page.context.cookies():
        if cookie["name"] == SESSION_COOKIE_NAME:
            return cookie
    return None


@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.critical
def test_login_with_valid_credentials_reaches_secure_area(
    login_page: LoginPage, page, base_url: str, credentials: Credentials
) -> None:
    """Шаги 1–5: вход на защищённую страницу с ожидаемым содержимым"""
    login_page.login(credentials.username, credentials.password)
    secure_page = SecurePage(page, base_url)

    # Шаг 3 — пользователь на защищённом маршруте
    expect(page).to_have_url(secure_page.url)
    expect(secure_page.flash).to_contain_text(LOGIN_SUCCESS_MESSAGE)
    expect(secure_page.flash_components.flash).to_have_class("flash success")
    assert secure_page.flash_components.flash_message() == LOGIN_SUCCESS_MESSAGE

    # Шаг 4 — заголовок и содержимое
    expect(page).to_have_title(EXPECTED_TITLE)
    expect(secure_page.heading).to_have_text("Secure Area")
    expect(secure_page.content).to_contain_text("Welcome to the Secure Area")
    # to_contain_text, не to_have_text: полный текст h4.subheader длиннее,
    # contain фиксирует смысловую часть и не ломается от мелких правок
    expect(secure_page.subheading).to_contain_text("Welcome to the Secure Area")

    # Шаг 5 — доступна ссылка Logout (<a>, не <button>. см. README)
    expect(secure_page.logout_button).to_be_visible()
    expect(secure_page.logout_button).to_be_enabled()
    expect(secure_page.logout_button).to_have_attribute("href", "/logout")


@pytest.mark.security
def test_authenticated_session_cookie_is_set(
    login_page: LoginPage, page, credentials: Credentials
) -> None:
    """После успешного входа в контексте есть HttpOnly cookie сессии"""
    login_page.login(credentials.username, credentials.password)
    expect(page).to_have_url(SecurePage(page, login_page.base_url).url)

    cookie = _session_cookie(page)
    assert cookie is not None, f"Missing {SESSION_COOKIE_NAME} after login"
    assert cookie.get("httpOnly") is True
    assert cookie.get("value"), "Session cookie value must be non-empty"


@pytest.mark.smoke
@pytest.mark.critical
def test_logout_returns_user_to_login_page(secure_page: SecurePage, page) -> None:
    """Шаги 6–7: выход завершает сессию и сообщает об этом"""
    session_before = _session_cookie(page)
    assert session_before is not None, f"Missing {SESSION_COOKIE_NAME} before logout"

    login_page = secure_page.logout()

    expect(page).to_have_url(login_page.url)
    expect(login_page.flash).to_contain_text(LOGOUT_SUCCESS_MESSAGE)
    assert login_page.flash_components.flash_message() == LOGOUT_SUCCESS_MESSAGE
    expect(login_page.submit_button).to_be_visible()

    session_after = _session_cookie(page)
    # Cookie может остаться, но значение сессии должно смениться после logout
    assert session_after is None or session_after["value"] != session_before["value"]


@pytest.mark.smoke
@pytest.mark.security
def test_secure_area_is_unreachable_after_logout(
    secure_page: SecurePage, page, base_url: str
) -> None:
    """Сессия завершена, а не просто переход на другую страницу"""
    secure_page.logout()

    SecurePage(page, base_url).open()
    login_page = LoginPage(page, base_url)

    expect(page).to_have_url(login_page.url)
    expect(login_page.flash).to_contain_text(MUST_LOGIN_MESSAGE)


@pytest.mark.smoke
def test_user_can_login_again_after_logout(
    secure_page: SecurePage, page, base_url: str, credentials: Credentials
) -> None:
    """После выхода повторный вход валидными кредами снова открывает /secure"""
    login_page = secure_page.logout()
    expect(page).to_have_url(login_page.url)

    login_page.login(credentials.username, credentials.password)
    secure_again = SecurePage(page, base_url)

    expect(page).to_have_url(secure_again.url)
    expect(secure_again.flash).to_have_class("flash success")
    expect(secure_again.logout_button).to_be_visible()
