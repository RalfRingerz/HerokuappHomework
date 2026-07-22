"""Page object главной страницы со списком всех примеров"""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.login_page import LoginPage


class MainPage(BasePage):
    path = "/"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.heading = page.locator("h1.heading")
        self.subheading = page.locator("h2")
        # Лента — это <img>, поэтому alt-текст — самый стабильный локатор.
        self.fork_me_ribbon = page.get_by_alt_text("Fork me on GitHub")
        # Ссылки на отдельные примеры, то есть содержимое страницы.
        self.example_links = page.locator("#content ul li a")
        self.footer_links = page.locator("#page-footer a")
        self.form_authentication_link = page.get_by_role(
            "link", name="Form Authentication"
        )

    def example_link_count(self) -> int:
        return self.example_links.count()

    def example_link_texts(self) -> list[str]:
        return [text.strip() for text in self.example_links.all_inner_texts()]

    def go_to_login_page(self) -> LoginPage:
        """Переходит по ссылке «Form Authentication» и возвращает следующую страницу"""
        self.form_authentication_link.click()
        return LoginPage(self.page, self.base_url)
