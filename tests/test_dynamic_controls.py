"""Сценарий 5 — страница с динамическими кнопками"""

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.dynamic_controls_page import DynamicControlsPage

pytestmark = [
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.positive,
]


def test_initial_page_state(dynamic_controls_page: DynamicControlsPage) -> None:
    """Начальное состояние страницы"""
    controls = dynamic_controls_page

    # Общие элементы страницы
    expect(controls.page).to_have_url(dynamic_controls_page.url)
    expect(controls.page_heading).to_be_visible()
    expect(controls.description).to_be_visible()
    expect(controls.checkbox_heading).to_be_visible()
    expect(controls.input_section_heading).to_be_visible()

    # Начальное состояние чекбокса
    expect(controls.checkbox).to_be_visible()
    expect(controls.checkbox).not_to_be_checked()
    expect(controls.checkbox_toggle_button).to_be_visible()
    expect(controls.checkbox_toggle_button).to_be_enabled()
    expect(controls.checkbox_toggle_button).to_have_text("Remove")
    expect(controls.checkbox_loading).to_have_count(0)

    # Начальное состояние текстового поля
    expect(controls.text_input).to_be_visible()
    expect(controls.text_input).to_be_empty()
    expect(controls.text_input).to_be_disabled()
    expect(controls.input_toggle_button).to_be_visible()
    expect(controls.input_toggle_button).to_have_text("Enable")
    expect(controls.input_loading).to_have_count(0)


def test_checkbox_can_be_checked_and_unchecked(
    dynamic_controls_page: DynamicControlsPage,
) -> None:
    """Установка и снятие чекбокса"""
    controls = dynamic_controls_page

    # Проверка что чекбокс не отмечен
    expect(controls.checkbox).not_to_be_checked()

    # Установка чекбокса и проверка того, что чекбокс отмечен
    controls.check_checkbox()
    expect(controls.checkbox).to_be_checked()

    # Снятие чекбокса и проверка того, что он снялся
    controls.uncheck_checkbox()
    expect(controls.checkbox).not_to_be_checked()

    # Проверка, что чекбокс по прежнему виден и доступен
    expect(controls.checkbox).to_be_visible()
    expect(controls.checkbox).to_be_enabled()


def test_checkbox_can_be_removed(dynamic_controls_page: DynamicControlsPage) -> None:
    """Удаление чекбокса"""
    controls = dynamic_controls_page

    # Удаление чекбокса через кнопку и проверки лоадера
    controls.remove_checkbox()
    controls.wait_for_checkbox_loading()
    expect(controls.checkbox_loading).to_have_text("Wait for it...")
    expect(controls.checkbox_toggle_button).to_be_disabled()

    # Проверки после завершения загрузки
    controls.wait_for_checkbox_loading_finished()
    expect(controls.checkbox_loading).to_have_count(0)
    expect(controls.checkbox).to_be_hidden()
    expect(controls.checkbox_message).to_have_text("It's gone!")

    # Проверка изменённого состояния кнопки
    expect(controls.checkbox_toggle_button).to_be_visible()
    expect(controls.checkbox_toggle_button).to_have_text("Add")


def test_checkbox_can_be_added(dynamic_controls_page: DynamicControlsPage) -> None:
    """Возвращение чекбокса"""
    controls = dynamic_controls_page

    # Удаление чекбокса и проверка что кнопка изменила надпись
    controls.remove_checkbox()
    controls.wait_for_checkbox_loading()
    controls.wait_for_checkbox_loading_finished()
    expect(controls.checkbox_toggle_button).to_have_text("Add")

    # Добавление чекбокса, проверка что кнопка недоступна во время загрузки
    controls.add_checkbox()
    controls.wait_for_checkbox_loading()
    expect(controls.checkbox_loading).to_have_text("Wait for it...")
    expect(controls.checkbox_toggle_button).to_be_disabled()
    controls.wait_for_checkbox_loading_finished()

    # Проверка что чекбокс появился и не отмечен
    expect(controls.checkbox).to_be_visible()
    expect(controls.checkbox).not_to_be_checked()
    expect(controls.checkbox_message).to_have_text("It's back!")
    expect(controls.checkbox_toggle_button).to_have_text("Remove")


@pytest.mark.parametrize(
    "value",
    [
        pytest.param("Playwright", id="text"),
        pytest.param("12345", id="digits"),
        pytest.param("Привет, мир!", id="unicode"),
    ],
)
def test_enabled_text_input_accepts_value(
    dynamic_controls_page: DynamicControlsPage, value
) -> None:
    """Активация и заполнение текстового поля"""
    controls = dynamic_controls_page

    # Проверка, что поле изначально заблокировано
    expect(controls.text_input).to_be_disabled()

    # Разблокировка поля и ожидание загрузки
    controls.enable_text_input()
    controls.wait_for_input_loading()
    expect(controls.input_loading).to_have_text("Wait for it...")
    expect(controls.input_toggle_button).to_be_disabled()
    controls.wait_for_input_loading_finished()

    # Проверка, что поле доступно и кнопка поменяла название
    expect(controls.text_input).to_be_enabled()
    expect(controls.input_message).to_have_text("It's enabled!")
    expect(controls.input_toggle_button).to_have_text("Disable")

    # Заполнение поля и проверка заполеннного значения
    controls.fill_text_input(value)
    expect(controls.text_input).to_have_value(value)


def test_text_input_can_be_disabled_and_preserves_value(
    dynamic_controls_page: DynamicControlsPage,
) -> None:
    """Блокировка поля с сохранением значения"""
    controls = dynamic_controls_page

    # Разблокировка поля и ожидание загрузки
    controls.enable_text_input()
    controls.wait_for_input_loading()
    expect(controls.input_loading).to_have_text("Wait for it...")
    expect(controls.input_toggle_button).to_be_disabled()
    controls.wait_for_input_loading_finished()

    # Заполнение инпута и проверка, что он заполнен
    content = "Hello!"
    controls.fill_text_input(content)
    expect(controls.text_input).to_have_value(content)

    # Блокировка инпута и ожидание завершения загрузки
    expect(controls.input_toggle_button).to_have_text("Disable")
    controls.disable_text_input()
    controls.wait_for_input_loading()
    expect(controls.input_loading).to_have_text("Wait for it...")
    expect(controls.input_toggle_button).to_be_disabled()
    controls.wait_for_input_loading_finished()

    # Проверка, что инпут заблокирован, отобразилось сообщение и изменилась кнопка
    expect(controls.text_input).to_be_disabled()
    expect(controls.input_message).to_have_text("It's disabled!")
    expect(controls.input_toggle_button).to_have_text("Enable")

    # Проверка, что даже после блокировки инпут остался заполнен
    expect(controls.text_input).to_have_value(content)
