"""Базовая страница: общее поведение для всех Page Object."""
from __future__ import annotations

import allure
from playwright.sync_api import Page

BASE_URL = "https://www.saucedemo.com"


class BasePage:
    path: str = "/"

    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> "BasePage":
        with allure.step(f"Открыть {self.path}"):
            self.page.goto(f"{BASE_URL}{self.path}", wait_until="domcontentloaded")
        return self

    def expect_loaded(self) -> "BasePage":
        """Каждая страница подтверждает, что действительно загрузилась."""
        with allure.step(f"Дождаться загрузки {type(self).__name__}"):
            self.page.wait_for_url(f"**{self.path}")
        return self

    @property
    def current_url(self) -> str:
        return self.page.url

    def screenshot(self, name: str) -> None:
        allure.attach(
            self.page.screenshot(full_page=True),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
