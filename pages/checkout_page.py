"""Оформление заказа: три шага — данные, сводка, подтверждение."""
from __future__ import annotations

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    path = "/checkout-step-one.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.first_name = page.locator("[data-test='firstName']")
        self.last_name = page.locator("[data-test='lastName']")
        self.postal_code = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.error = page.locator("[data-test='error']")

    @allure.step("Заполнить данные покупателя: {first} {last}, индекс {postal}")
    def fill_details(self, first: str, last: str, postal: str) -> "CheckoutPage":
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        return self

    @allure.step("Продолжить")
    def submit(self) -> "CheckoutOverviewPage":
        self.continue_button.click()
        return CheckoutOverviewPage(self.page)

    @property
    def error_text(self) -> str:
        return self.error.inner_text()


class CheckoutOverviewPage(BasePage):
    path = "/checkout-step-two.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.subtotal = page.locator("[data-test='subtotal-label']")
        self.tax = page.locator("[data-test='tax-label']")
        self.total = page.locator("[data-test='total-label']")
        self.finish_button = page.locator("[data-test='finish']")
        self.names = page.locator(".inventory_item_name")

    @allure.step("Завершить заказ")
    def finish(self) -> "CheckoutCompletePage":
        self.finish_button.click()
        return CheckoutCompletePage(self.page)

    @staticmethod
    def _amount(text: str) -> float:
        return float(text.split("$")[1])

    @property
    def subtotal_value(self) -> float:
        return self._amount(self.subtotal.inner_text())

    @property
    def tax_value(self) -> float:
        return self._amount(self.tax.inner_text())

    @property
    def total_value(self) -> float:
        return self._amount(self.total.inner_text())

    @property
    def titles(self) -> list[str]:
        return self.names.all_inner_texts()


class CheckoutCompletePage(BasePage):
    path = "/checkout-complete.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header = page.locator("[data-test='complete-header']")

    @property
    def header_text(self) -> str:
        return self.header.inner_text()
