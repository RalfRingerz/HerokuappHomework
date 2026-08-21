"""Сценарий 4 — страница с ховерами"""

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.hovers_page import HoversPage

pytestmark = [
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.positive,
]


def test_initial_page_state(hovers_page: HoversPage) -> None:
    """Начальное состояние страницы"""
    # Проверка общих элементов страницы
    expect(hovers_page.page).to_have_url(hovers_page.url)
    expect(hovers_page.heading).to_be_visible()
    expect(hovers_page.page_description).to_be_visible()
    expect(hovers_page.figure).to_have_count(3)


def test_info_hidded_before_hover(hovers_page: HoversPage) -> None:
    """Информация скрыта до наведения"""
    # Проверка начального состояния карточек
    expect(hovers_page.figure).to_have_count(3)

    # Проверка, что информация скрыта до наведения
    for index in range(3):
        username = hovers_page.get_username(index)
        profile_link = hovers_page.get_profile_link(index)

        expect(username).to_be_hidden()
        expect(profile_link).to_be_hidden()


@pytest.mark.parametrize(
    "index, expected_name, expected_href",
    [
        pytest.param(0, "name: user1", "/users/1", id="user-1"),
        pytest.param(1, "name: user2", "/users/2", id="user-2"),
        pytest.param(2, "name: user3", "/users/3", id="user-3"),
    ],
)
def test_user_information_after_hover(
    hovers_page: HoversPage, index: int, expected_name: str, expected_href: str
) -> None:
    """Информация появляется после ховера"""
    # Проверка начального состояния карточек
    expect(hovers_page.figure).to_have_count(3)

    # Получение элементов выбранного пользователя
    username = hovers_page.get_username(index)
    profile_link = hovers_page.get_profile_link(index)

    # Наведение на карточку пользователя
    hovers_page.hover_figure(index)

    # Проверка появившейся информации
    expect(username).to_be_visible()
    expect(username).to_have_text(expected_name)

    # Проверка появившейся информации
    expect(profile_link).to_be_visible()
    expect(profile_link).to_have_attribute("href", expected_href)


def test_only_hovered_user_information_is_visible(hovers_page: HoversPage) -> None:
    """Информация остальных пользователей остаётся скрытой"""
    # Проверка начального состояния карточек
    expect(hovers_page.figure).to_have_count(3)

    # Получение элементов выбранного пользователя
    active_username = hovers_page.get_username(0)
    active_profile_link = hovers_page.get_profile_link(0)

    # Наведение на карточку пользователя
    hovers_page.hover_figure(0)

    # Проверка появившейся информации
    expect(active_username).to_be_visible()
    expect(active_profile_link).to_be_visible()

    # Проверка остальных карточек
    for index in range(1, 3):
        inactive_username = hovers_page.get_username(index)
        inactive_profile_link = hovers_page.get_profile_link(index)

        expect(inactive_username).to_be_hidden()
        expect(inactive_profile_link).to_be_hidden()


def test_user_information_is_hidden_after_mouse_leaves(hovers_page: HoversPage) -> None:
    """Информация скрывается после ухода курсора"""
    # Проверка начального состояния карточек
    expect(hovers_page.figure).to_have_count(3)

    # Получение элементов выбранного пользователя
    username = hovers_page.get_username(0)
    profile_link = hovers_page.get_profile_link(0)

    # Наведение на карточку пользователя
    hovers_page.hover_figure(0)

    # Проверка появившейся информации
    expect(username).to_be_visible()
    expect(profile_link).to_be_visible()

    # Перемещение курсора за пределы карточки
    hovers_page.heading.hover()

    # Проверка, что информацию не видно
    expect(username).to_be_hidden()
    expect(profile_link).to_be_hidden()


@pytest.mark.parametrize(
    "index, expected_path",
    [
        pytest.param(0, "/users/1", id="user-1"),
        pytest.param(1, "/users/2", id="user-2"),
        pytest.param(2, "/users/3", id="user-3"),
    ],
)
def test_profile_link_navigation(
    hovers_page: HoversPage,
    index: int,
    expected_path: str
) -> None:
    """Переход по ссылке профиля"""
    # Переход по ссылке профиля
    hovers_page.open_profile(index)

    # Ожидаемый урл
    expected_url = f"{hovers_page.base_url}{expected_path}"

    # Проверка, что попали на ожидаемую страницу
    expect(hovers_page.page).to_have_url(expected_url)
