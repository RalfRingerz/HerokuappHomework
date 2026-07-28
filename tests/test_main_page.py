"""Сценарий 1 — главная страница"""

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.main_page import MainPage

pytestmark = [
    pytest.mark.ui,
    pytest.mark.e2e,
    pytest.mark.regression,
    pytest.mark.positive,
]

EXPECTED_TITLE = "The Internet"
EXPECTED_GITHUB_RIBBON_URL = "https://github.com/tourdedave/the-internet"
# Количество ссылок на примеры, которое ожидает ТЗ.
# Как это число было проверено — см. README в разделе «Замечания по ТЗ»
EXPECTED_EXAMPLE_LINKS = 44
# Пересчёт всех <a> на странице: 44 каталога + риббон GitHub + футер
EXPECTED_TOTAL_PAGE_LINKS = 46
EXPECTED_FOOTER_LINKS = 1


@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.critical
def test_main_page_opens_at_base_url(main_page: MainPage, base_url: str) -> None:
    """После открытия URL совпадает с base URL главной страницы"""
    expect(main_page.page).to_have_url(f"{base_url}/")


@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.critical
def test_main_page_has_title(main_page: MainPage) -> None:
    """Страница имеет ожидаемый заголовок документа"""
    expect(main_page.page).to_have_title(EXPECTED_TITLE)


@pytest.mark.smoke
def test_main_page_shows_heading(main_page: MainPage) -> None:
    expect(main_page.heading).to_be_visible()
    expect(main_page.heading).to_have_text("Welcome to the-internet")


def test_main_page_shows_subheading(main_page: MainPage) -> None:
    """Подзаголовок каталога примеров виден и подписан"""
    expect(main_page.subheading).to_be_visible()
    expect(main_page.subheading).to_have_text("Available Examples")


@pytest.mark.smoke
@pytest.mark.critical
def test_main_page_has_fork_me_ribbon(main_page: MainPage) -> None:
    """Лента «Fork me on GitHub» присутствует и видна"""
    expect(main_page.fork_me_ribbon).to_be_visible()


def test_fork_me_ribbon_links_to_project_github(main_page: MainPage) -> None:
    """Лента — ссылка на репозиторий (img может быть visible при hidden <a>)"""
    expect(main_page.fork_me_link).to_have_attribute("href", EXPECTED_GITHUB_RIBBON_URL)
    expect(main_page.fork_me_link).to_be_attached()


@pytest.mark.smoke
@pytest.mark.critical
def test_main_page_lists_expected_number_of_examples(main_page: MainPage) -> None:
    """Каталог примеров содержит ожидаемое количество ссылок"""
    expect(main_page.example_links).to_have_count(EXPECTED_EXAMPLE_LINKS)


@pytest.mark.smoke
def test_form_authentication_link_present_in_catalog(main_page: MainPage) -> None:
    """В каталоге есть «Form Authentication» с путём на страницу входа"""
    link = main_page.example_link("Form Authentication")
    expect(link).to_be_visible()
    expect(link).to_have_attribute("href", "/login")


def test_main_page_total_links_include_chrome_outside_catalog(
    main_page: MainPage,
) -> None:
    """44 ссылки в каталоге; всего 46 <a> — риббон и футер сверх каталога"""
    expect(main_page.footer_links).to_have_count(EXPECTED_FOOTER_LINKS)
    expect(main_page.page.locator("a")).to_have_count(EXPECTED_TOTAL_PAGE_LINKS)


def test_example_links_have_visible_text(main_page: MainPage) -> None:
    """Ни одна ссылка без видимой подписи — проверка на битую разметку"""
    blank = [i for i, text in enumerate(main_page.example_link_texts()) if not text]
    assert not blank, f"Links with empty text at positions: {blank}"


def test_example_links_have_unique_text_and_non_empty_href(
    main_page: MainPage,
) -> None:
    """Пункты каталога без дублей по тексту и с непустым href"""
    texts = main_page.example_link_texts()
    hrefs = main_page.example_link_hrefs()

    empty_href = [i for i, href in enumerate(hrefs) if not href.strip()]
    assert not empty_href, f"Links with empty href at positions: {empty_href}"

    duplicates = sorted({t for t in texts if texts.count(t) > 1})
    assert not duplicates, f"Duplicate example link texts: {duplicates}"
