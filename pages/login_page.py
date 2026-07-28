"""Page object страницы формы аутентификации"""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage, FlashComponents


class LoginPage(BasePage):
    path = "/login"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.flash = page.locator("#flash")
        self.flash_components = FlashComponents(self.flash)
        self.heading = page.locator("h2")
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.submit_button = page.get_by_role("button", name="Login")

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
        return self.flash_components.flash_message()
