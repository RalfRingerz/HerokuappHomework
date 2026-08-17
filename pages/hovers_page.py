"""Page Object для страницы с ховерами /hovers"""

from __future__ import annotations

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class HoversPage(BasePage):
    path = "/hovers"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.heading = page.get_by_role("heading", name="Hovers")
        self.page_description = page.get_by_text(
            "Hover over the image for additional information"
        )
        self.figure = page.locator(".figure")

    def get_figure(self, index: int) -> Locator:
        """
        Возвращает объект, аватарку пользователя по индексу, их всего 3
        Объекты .figure от 0 до 2
        """
        return self.figure.nth(index)

    def get_username(self, index: int) -> Locator:
        """Возвращает имя пользователя по индексу"""
        return self.get_figure(index).locator(".figcaption h5")

    def get_profile_link(self, index: int) -> Locator:
        """Возвращает ссылку на профиль пользователя по индексу"""
        return self.get_figure(index).get_by_role("link", name="View profile")

    def hover_figure(self, index: int) -> None:
        """Воспроизведение ховера по нужному индексу юзера"""
        self.get_figure(index).hover()

    def open_profile(self, index: int) -> None:
        """Открытие профиля юзера через кнопку "View profile" """
        self.hover_figure(index)
        self.get_profile_link(index).click()
