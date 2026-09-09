"""Корзина."""
from __future__ import annotations

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    path = "/cart.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.items = page.locator("[data-test='inventory-item']")
        self.names = page.locator(".inventory_item_name")
        self.checkout = page.locator("[data-test='checkout']")
        self.continue_shopping = page.locator("[data-test='continue-shopping']")

    @allure.step("Перейти к оформлению")
    def start_checkout(self):
        from pages.checkout_page import CheckoutPage

        self.checkout.click()
        return CheckoutPage(self.page)

    @property
    def titles(self) -> list[str]:
        return self.names.all_inner_texts()
