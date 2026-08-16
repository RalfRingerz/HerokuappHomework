"""Page Object для страницы с динамическими кнопками /dynamic_controls"""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class DynamicControlsPage(BasePage):
    path = "/dynamic_controls"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.page_heading = page.get_by_role("heading", name="Dynamic Controls")
        self.description = page.get_by_text(
            "This example demonstrates when elements "
            "(e.g., checkbox, input field, etc.) are changed asynchronously."
        )

        self.checkbox_heading = page.get_by_role("heading", name="Remove/add")
        self.checkbox_form = page.locator("#checkbox-example")
        self.checkbox = self.checkbox_form.locator('input[type="checkbox"]')
        self.checkbox_toggle_button = self.checkbox_form.get_by_role("button")
        self.checkbox_loading = self.checkbox_form.locator("#loading:visible")
        self.checkbox_message = self.checkbox_form.locator("#message")

        self.input_section_heading = page.get_by_role("heading", name="Enable/disable")
        self.input_form = page.locator("#input-example")
        self.text_input = self.input_form.locator('input[type="text"]')
        self.input_toggle_button = self.input_form.get_by_role("button")
        self.input_loading = self.input_form.locator("#loading:visible")
        self.input_message = self.input_form.locator("#message")

    def remove_checkbox(self) -> None:
        self.checkbox_toggle_button.click()

    def add_checkbox(self) -> None:
        self.checkbox_toggle_button.click()

    def check_checkbox(self) -> None:
        self.checkbox.check()

    def uncheck_checkbox(self) -> None:
        self.checkbox.uncheck()

    def enable_text_input(self) -> None:
        self.input_toggle_button.click()

    def disable_text_input(self) -> None:
        self.input_toggle_button.click()

    def fill_text_input(self, value: str) -> None:
        self.text_input.fill(value)

    def clear_text_input(self) -> None:
        self.text_input.clear()

    def wait_for_checkbox_loading(self) -> None:
        self.checkbox_loading.wait_for(state="visible")

    def wait_for_checkbox_loading_finished(self) -> None:
        self.checkbox_loading.wait_for(state="hidden")

    def wait_for_input_loading(self) -> None:
        self.input_loading.wait_for(state="visible")

    def wait_for_input_loading_finished(self) -> None:
        self.input_loading.wait_for(state="hidden")
