"""Общее поведение, разделяемое всеми page object'ами

Page object'ы предоставляют локаторы и действия с понятным намерением. Они не
содержат assert'ов, проверки живут в тестах, чтобы падение указывало на
требование, а не на вспомогательный код
"""

from __future__ import annotations

from playwright.sync_api import Locator, Page


class BasePage:
    """Базовый класс для всех page object'ов.

    Подклассы задают 'path', это маршрут относительно настроенного base URL
    """

    path: str = "/"

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    @property
    def url(self) -> str:
        """Абсолютный URL этой страницы для текущего окружения"""
        return f"{self.base_url}{self.path}"

    def open(self):
        """Переходит на страницу и возвращает self для цепочки вызовов"""
        self.page.goto(self.url)
        return self

    @property
    def title(self) -> str:
        return self.page.title()

    @property
    def current_url(self) -> str:
        return self.page.url


class FlashComponents:
    def __init__(self, flash: Locator) -> None:
        self.flash = flash

    def flash_message(self) -> str:
        """Текст flash-баннера без символа закрытия в конце"""
        return self.flash.inner_text().replace("×", "").strip()

    def flash_class(self) -> str:
        """Значение атрибута class у flash-баннера (например 'flash error')"""
        return self.flash.get_attribute("class") or ""

