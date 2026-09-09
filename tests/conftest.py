"""Фикстуры и хуки: авторизация, размер окна, скриншот при падении."""
from __future__ import annotations

from typing import Any, Generator

import allure
import pytest
from playwright.sync_api import Page

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

STANDARD_USER = "standard_user"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict[str, Any]) -> dict[str, Any]:
    """Единый вьюпорт для всех прогонов, иначе вёрстка «плавает» между машинами."""
    return {**browser_context_args, "viewport": {"width": 1440, "height": 900}}


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page).open()


@pytest.fixture
def inventory_page(login_page: LoginPage) -> InventoryPage:
    """Каталог под обычным пользователем — стартовая точка большинства тестов."""
    return login_page.login(STANDARD_USER).expect_loaded()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator:
    """Кладёт в отчёт скриншот и HTML страницы, если тест упал."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page: Page | None = item.funcargs.get("page")
    if page is None or page.is_closed():
        return

    allure.attach(
        page.screenshot(full_page=True),
        name="Скриншот в момент падения",
        attachment_type=allure.attachment_type.PNG,
    )
    allure.attach(
        page.content(),
        name="HTML страницы",
        attachment_type=allure.attachment_type.HTML,
    )
    allure.attach(page.url, name="URL", attachment_type=allure.attachment_type.TEXT)
