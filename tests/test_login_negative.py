"""Сценарий 2 — вход: неверные учётные данные не должны проходить"""

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from config import Credentials, get_credentials
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.secure_page import SecurePage

pytestmark = [
    pytest.mark.ui,
    pytest.mark.e2e,
    pytest.mark.regression,
    pytest.mark.login,
    pytest.mark.auth,
]

INVALID_USERNAME_MESSAGE = "Your username is invalid!"
INVALID_PASSWORD_MESSAGE = "Your password is invalid!"
MUST_LOGIN_MESSAGE = "You must login to view the secure area!"

_credentials = get_credentials()


@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.critical
@pytest.mark.positive
def test_navigate_to_login_page_from_main_page(main_page: MainPage) -> None:
    """Страница входа доступна по ссылке «Form Authentication» и имеет форму"""
    login_page = main_page.go_to_login_page()

    expect(login_page.page).to_have_url(login_page.url)
    expect(login_page.heading).to_have_text("Login Page")
    expect(login_page.username_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()
    expect(login_page.password_input).to_have_attribute("type", "password")
    expect(login_page.submit_button).to_be_visible()


@pytest.mark.negative
@pytest.mark.parametrize(
    "username, password, expected_message",
    [
        pytest.param(
            "wronguser",
            _credentials.password,
            INVALID_USERNAME_MESSAGE,
            id="unknown-username",
        ),
        pytest.param(
            _credentials.username,
            "wrongpassword",
            INVALID_PASSWORD_MESSAGE,
            id="wrong-password",
        ),
        pytest.param(
            "wronguser",
            "wrongpassword",
            INVALID_USERNAME_MESSAGE,
            id="both-wrong",
        ),
        pytest.param("", "", INVALID_USERNAME_MESSAGE, id="both-empty"),
        pytest.param(
            "",
            _credentials.password,
            INVALID_USERNAME_MESSAGE,
            id="empty-username",
        ),
        pytest.param(
            _credentials.username,
            "",
            INVALID_PASSWORD_MESSAGE,
            id="empty-password",
        ),
        pytest.param(
            _credentials.username.swapcase(),
            _credentials.password,
            INVALID_USERNAME_MESSAGE,
            id="username-wrong-case",
        ),
        pytest.param(
            f" {_credentials.username} ",
            _credentials.password,
            INVALID_USERNAME_MESSAGE,
            id="username-padded",
        ),
        pytest.param(
            _credentials.username,
            _credentials.password.upper(),
            INVALID_PASSWORD_MESSAGE,
            id="password-wrong-case",
        ),
        pytest.param(
            _credentials.username,
            _credentials.password + " ",
            INVALID_PASSWORD_MESSAGE,
            id="password-trailing-space",
        ),
        pytest.param(
            "' OR '1'='1",
            "' OR '1'='1",
            INVALID_USERNAME_MESSAGE,
            id="sql-injection-attempt",
            marks=pytest.mark.security,
        ),
        pytest.param(
            "<script>alert(1)</script>",
            _credentials.password,
            INVALID_USERNAME_MESSAGE,
            id="xss-attempt",
            marks=pytest.mark.security,
        ),
    ],
)
def test_login_rejected_with_invalid_credentials(
    login_page: LoginPage, username: str, password: str, expected_message: str
) -> None:
    """Неверные учётные данные выводят ошибку и не аутентифицируют пользователя"""
    login_page.login(username, password)

    expect(login_page.flash).to_contain_text(expected_message)
    expect(login_page.flash).to_have_class("flash error")
    expect(login_page.page).to_have_url(login_page.url)
    expect(login_page.submit_button).to_be_visible()


# Exact flash + очистка полей — на двух представителях
@pytest.mark.negative
@pytest.mark.parametrize(
    "username, password, expected_message",
    [
        pytest.param(
            "wronguser",
            _credentials.password,
            INVALID_USERNAME_MESSAGE,
            id="unknown-username-strict",
        ),
        pytest.param(
            _credentials.username,
            "wrongpassword",
            INVALID_PASSWORD_MESSAGE,
            id="wrong-password-strict",
        ),
    ],
)
def test_failed_login_exact_flash_and_cleared_fields(
    login_page: LoginPage, username: str, password: str, expected_message: str
) -> None:
    """После отказа: точный текст ошибки и пустые поля формы"""
    login_page.login(username, password)

    assert login_page.flash_message() == expected_message
    expect(login_page.username_input).to_have_value("")
    expect(login_page.password_input).to_have_value("")


@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_failed_login_does_not_create_authenticated_session(
    login_page: LoginPage, page, base_url: str, credentials: Credentials
) -> None:
    """После неверного пароля прямой заход на /secure снова требует логин"""
    login_page.login(credentials.username, "definitely-wrong-password")
    expect(login_page.flash).to_have_class("flash error")

    SecurePage(page, base_url).open()
    redirected = LoginPage(page, base_url)

    expect(page).to_have_url(redirected.url)
    expect(redirected.flash).to_contain_text(MUST_LOGIN_MESSAGE)


@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
@pytest.mark.critical
def test_secure_area_is_not_reachable_without_login(page, base_url: str) -> None:
    """Прямой переход на защищённый маршрут возвращает на страницу входа"""
    SecurePage(page, base_url).open()
    login_page = LoginPage(page, base_url)

    expect(page).to_have_url(login_page.url)
    expect(login_page.flash).to_contain_text(MUST_LOGIN_MESSAGE)


@pytest.mark.negative
@pytest.mark.security
def test_error_message_does_not_reveal_which_field_was_wrong_for_unknown_user(
    login_page: LoginPage, credentials: Credentials
) -> None:
    """Неизвестный логин с верным паролем не выдаёт, что пароль был правильным

    Фиксирует текущее поведение: приложение отвечает «username is invalid»
    до проверки пароля. Обратная утечка, что известный логин с неверным
    паролем получает «password is invalid» и тем самым подтверждает существование
    логина, описана в README («Наблюдение по безопасности»). Здесь проверяется
    только отсутствие лишней информации о пароле для неизвестного логина
    """
    login_page.login("definitely-not-a-user", credentials.password)

    # Сравниваем строку целиком: expect().to_contain_text() прошёл бы и при
    # «Your username is invalid! Password was correct.» — лишний текст не отловит
    assert login_page.flash_message() == INVALID_USERNAME_MESSAGE
