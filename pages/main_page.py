"""Page object главной страницы со списком всех примеров"""

from __future__ import annotations

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage
from pages.login_page import LoginPage


class MainPage(BasePage):
    path = "/"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.heading = page.locator("h1.heading")
        self.subheading = page.locator("h2")
        # Лента это <img>, поэтому alt-текст это самый стабильный локатор
        self.fork_me_ribbon = page.get_by_alt_text("Fork me on GitHub")
        # Сама ссылка: role + name стабильнее, чем CSS обёртка вокруг img
        # (у <a> иногда нулевой box, и to_be_visible падает при живом img)
        self.fork_me_link = page.get_by_role("link", name="Fork me on GitHub")
        # Ссылки на отдельные примеры, то есть содержимое страницы
        self.example_links = page.locator("#content ul li a")
        self.footer_links = page.locator("#page-footer a")
        self.form_authentication_link = page.get_by_role(
            "link", name="Form Authentication"
        )

    def example_link_count(self) -> int:
        return self.example_links.count()

    def example_link_texts(self) -> list[str]:
        return [text.strip() for text in self.example_links.all_inner_texts()]

    def example_link_hrefs(self) -> list[str]:
        """href каждого пункта каталога (как в DOM, относительные)"""
        return [
            href or ""
            for href in self.example_links.evaluate_all(
                "els => els.map(el => el.getAttribute('href'))"
            )
        ]

    def example_link(self, name: str) -> Locator:
        """Ссылка каталога по видимому тексту"""
        return self.example_links.filter(has_text=name)

    def go_to_login_page(self) -> LoginPage:
        """Переходит по ссылке «Form Authentication» и возвращает следующую страницу"""
        self.form_authentication_link.click()
        return LoginPage(self.page, self.base_url)
