"""Страница авторизации."""
from __future__ import annotations

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage

PASSWORD = "secret_sauce"


class LoginPage(BasePage):
    path = "/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.submit = page.locator("#login-button")
        self.error = page.locator("[data-test='error']")

    @allure.step("Войти под пользователем «{user}»")
    def login(self, user: str, password: str = PASSWORD) -> InventoryPage:
        self.username.fill(user)
        self.password.fill(password)
        self.submit.click()
        return InventoryPage(self.page)

    @allure.step("Отправить форму с логином «{user}» и паролем «{password}»")
    def try_login(self, user: str, password: str) -> "LoginPage":
        self.username.fill(user)
        self.password.fill(password)
        self.submit.click()
        return self

    @property
    def error_text(self) -> str:
        return self.error.inner_text()
