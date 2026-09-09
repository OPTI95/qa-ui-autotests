"""Каталог: сортировка, добавление в корзину, счётчик."""
from __future__ import annotations

import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@allure.epic("SauceDemo")
@allure.feature("Каталог")
class TestInventory:
    @allure.story("Отображение")
    @allure.title("В каталоге шесть товаров, у каждого есть имя и цена")
    @pytest.mark.smoke
    def test_catalog_is_complete(self, inventory_page: InventoryPage) -> None:
        assert inventory_page.items.count() == 6
        assert all(inventory_page.titles), "У товара пустое название"
        assert all(price > 0 for price in inventory_page.price_values)

    @allure.story("Корзина")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Счётчик корзины растёт при добавлении товаров")
    @pytest.mark.smoke
    def test_cart_badge_counts_items(self, inventory_page: InventoryPage) -> None:
        assert inventory_page.cart_count == 0

        inventory_page.add_to_cart(BACKPACK)
        assert inventory_page.cart_count == 1

        inventory_page.add_to_cart(BIKE_LIGHT)
        assert inventory_page.cart_count == 2

    @allure.story("Корзина")
    @allure.title("Удаление товара возвращает счётчик обратно")
    @pytest.mark.regression
    def test_remove_item_updates_badge(self, inventory_page: InventoryPage) -> None:
        inventory_page.add_to_cart(BACKPACK)

        inventory_page.remove_from_cart(BACKPACK)

        assert inventory_page.cart_count == 0, "Счётчик не обнулился после удаления"

    @allure.story("Сортировка")
    @allure.title("Сортировка по цене «{option}» выстраивает товары верно")
    @pytest.mark.regression
    @pytest.mark.parametrize("option, reverse", [("lohi", False), ("hilo", True)])
    def test_sort_by_price(
        self, inventory_page: InventoryPage, option: str, reverse: bool
    ) -> None:
        inventory_page.sort_by(option)

        prices = inventory_page.price_values
        assert prices == sorted(prices, reverse=reverse), f"Неверный порядок: {prices}"

    @allure.story("Сортировка")
    @allure.title("Сортировка по имени «{option}» выстраивает товары верно")
    @pytest.mark.regression
    @pytest.mark.parametrize("option, reverse", [("az", False), ("za", True)])
    def test_sort_by_name(
        self, inventory_page: InventoryPage, option: str, reverse: bool
    ) -> None:
        inventory_page.sort_by(option)

        titles = inventory_page.titles
        assert titles == sorted(titles, reverse=reverse), f"Неверный порядок: {titles}"


@allure.epic("SauceDemo")
@allure.feature("Дефекты стенда")
class TestKnownDefects:
    """Тесты, воспроизводящие намеренно сломанное поведение problem_user."""

    @allure.story("problem_user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("BUG-101: у problem_user все карточки показывают одну картинку")
    @pytest.mark.defect
    @pytest.mark.xfail(
        reason="BUG-101: все шесть товаров отдают один и тот же src изображения",
        strict=True,
    )
    def test_product_images_are_unique(self, login_page: LoginPage) -> None:
        inventory = login_page.login("problem_user").expect_loaded()

        sources = inventory.image_sources

        assert len(set(sources)) == len(sources), (
            f"Ожидали 6 разных изображений, уникальных: {len(set(sources))}"
        )

    @allure.story("problem_user")
    @allure.title("BUG-102: у problem_user не работает сортировка")
    @pytest.mark.defect
    @pytest.mark.xfail(
        reason="BUG-102: выбор варианта сортировки не меняет порядок товаров",
        strict=True,
    )
    def test_sorting_works_for_problem_user(self, login_page: LoginPage) -> None:
        inventory = login_page.login("problem_user").expect_loaded()

        inventory.sort_by("za")

        titles = inventory.titles
        assert titles == sorted(titles, reverse=True), f"Порядок не изменился: {titles}"
