"""Page object защищённой области после аутентификации"""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage, FlashComponents
from pages.login_page import LoginPage


class SecurePage(BasePage):
    # В ТЗ указан маршрут "/security"; приложение отдаёт страницу по "/secure" !!!
    # Подробнее в README, раздел «Замечания по ТЗ»
    path = "/secure"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.heading = page.locator("h2")
        self.flash = page.locator("#flash")
        self.flash_components = FlashComponents(self.flash)
        self.subheading = page.locator("h4.subheader")
        self.content = page.locator("#content")
        # В ТЗ «Logout button», НО фактически это <a>, не <button> !!!
        self.logout_button = page.get_by_role("link", name="Logout")

    def logout(self) -> LoginPage:
        self.logout_button.click()
        return LoginPage(self.page, self.base_url)


