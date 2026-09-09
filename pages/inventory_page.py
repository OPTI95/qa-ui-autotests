"""Каталог товаров."""
from __future__ import annotations

import re

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


def _slug(title: str) -> str:
    """«Sauce Labs Backpack» -> «sauce-labs-backpack» для data-test кнопок."""
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


class InventoryPage(BasePage):
    path = "/inventory.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.items = page.locator("[data-test='inventory-item']")
        self.names = page.locator(".inventory_item_name")
        self.prices = page.locator(".inventory_item_price")
        self.images = page.locator(".inventory_item_img img")
        self.sort = page.locator("[data-test='product-sort-container']")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")

    @allure.step("Добавить в корзину «{title}»")
    def add_to_cart(self, title: str) -> "InventoryPage":
        self.page.click(f"[data-test='add-to-cart-{_slug(title)}']")
        return self

    @allure.step("Убрать из корзины «{title}»")
    def remove_from_cart(self, title: str) -> "InventoryPage":
        self.page.click(f"[data-test='remove-{_slug(title)}']")
        return self

    @allure.step("Отсортировать: {option}")
    def sort_by(self, option: str) -> "InventoryPage":
        self.sort.select_option(option)
        return self

    @allure.step("Перейти в корзину")
    def open_cart(self):
        from pages.cart_page import CartPage

        self.cart_link.click()
        return CartPage(self.page)

    @property
    def titles(self) -> list[str]:
        return self.names.all_inner_texts()

    @property
    def price_values(self) -> list[float]:
        return [float(p.lstrip("$")) for p in self.prices.all_inner_texts()]

    @property
    def cart_count(self) -> int:
        return int(self.cart_badge.inner_text()) if self.cart_badge.count() else 0

    @property
    def image_sources(self) -> list[str]:
        return self.images.evaluate_all("els => els.map(e => e.getAttribute('src'))")
