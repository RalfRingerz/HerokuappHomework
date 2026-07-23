"""Page object страницы формы аутентификации"""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/login"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.heading = page.locator("h2")
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.submit_button = page.get_by_role("button", name="Login")
        self.flash = page.locator("#flash")

    def login(self, username: str, password: str) -> None:
        """Заполняет форму и отправляет её.
        Намеренно не ждёт конкретного исхода: вызывающий код сам решает,
        ожидается успех или ошибка
        """
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_button.click()

    def flash_message(self) -> str:
        """Текст flash-баннера без символа закрытия в конце"""
        return self.flash.inner_text().replace("×", "").strip()

    def flash_class(self) -> str:
        """Значение атрибута class у flash-баннера (например 'flash error')"""
        return self.flash.get_attribute("class") or ""
