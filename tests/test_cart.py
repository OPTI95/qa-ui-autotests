"""Корзина: состав и переходы."""
from __future__ import annotations

import allure
import pytest

from pages.inventory_page import InventoryPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@allure.epic("SauceDemo")
@allure.feature("Корзина")
class TestCart:
    @allure.story("Состав корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("В корзину попадают именно выбранные товары")
    @pytest.mark.smoke
    def test_cart_contains_selected_items(
        self, inventory_page: InventoryPage
    ) -> None:
        inventory_page.add_to_cart(BACKPACK).add_to_cart(BIKE_LIGHT)

        cart = inventory_page.open_cart().expect_loaded()

        assert sorted(cart.titles) == sorted([BACKPACK, BIKE_LIGHT])

    @allure.story("Состав корзины")
    @allure.title("Пустая корзина не содержит позиций")
    @pytest.mark.regression
    def test_empty_cart_has_no_items(self, inventory_page: InventoryPage) -> None:
        cart = inventory_page.open_cart().expect_loaded()

        assert cart.items.count() == 0

    @allure.story("Навигация")
    @allure.title("«Continue shopping» возвращает в каталог без потери корзины")
    @pytest.mark.regression
    def test_continue_shopping_keeps_cart(
        self, inventory_page: InventoryPage
    ) -> None:
        inventory_page.add_to_cart(BACKPACK)
        cart = inventory_page.open_cart().expect_loaded()

        cart.continue_shopping.click()

        inventory_page.expect_loaded()
        assert inventory_page.cart_count == 1, "Корзина обнулилась при возврате"
