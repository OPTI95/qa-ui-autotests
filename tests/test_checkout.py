"""Оформление заказа: сквозной сценарий, валидация и расчёт сумм."""
from __future__ import annotations

import allure
import pytest

from pages.inventory_page import InventoryPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"
TAX_RATE = 0.08


@allure.epic("SauceDemo")
@allure.feature("Оформление заказа")
class TestCheckout:
    @allure.story("Сквозной сценарий")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Полный путь от каталога до подтверждения заказа")
    @pytest.mark.smoke
    def test_full_purchase_flow(self, inventory_page: InventoryPage) -> None:
        inventory_page.add_to_cart(BACKPACK)

        overview = (
            inventory_page.open_cart()
            .expect_loaded()
            .start_checkout()
            .expect_loaded()
            .fill_details("Ivan", "Petrov", "364000")
            .submit()
            .expect_loaded()
        )
        assert overview.titles == [BACKPACK]

        complete = overview.finish().expect_loaded()

        assert complete.header_text == "Thank you for your order!"

    @allure.story("Расчёт сумм")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Итог равен сумме позиций плюс налог 8%")
    @pytest.mark.regression
    def test_total_equals_subtotal_plus_tax(
        self, inventory_page: InventoryPage
    ) -> None:
        inventory_page.add_to_cart(BACKPACK).add_to_cart(BIKE_LIGHT)

        overview = (
            inventory_page.open_cart()
            .expect_loaded()
            .start_checkout()
            .expect_loaded()
            .fill_details("Ivan", "Petrov", "364000")
            .submit()
            .expect_loaded()
        )

        expected_tax = round(overview.subtotal_value * TAX_RATE, 2)
        assert overview.tax_value == expected_tax, "Налог посчитан неверно"
        assert overview.total_value == round(
            overview.subtotal_value + overview.tax_value, 2
        ), "Итоговая сумма не сходится"

    @allure.story("Валидация формы")
    @allure.title("Пропущенное поле «{missing}» блокирует оформление")
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "first, last, postal, missing, message",
        [
            ("", "Petrov", "364000", "имя", "Error: First Name is required"),
            ("Ivan", "", "364000", "фамилия", "Error: Last Name is required"),
            ("Ivan", "Petrov", "", "индекс", "Error: Postal Code is required"),
        ],
    )
    def test_required_fields_validated(
        self,
        inventory_page: InventoryPage,
        first: str,
        last: str,
        postal: str,
        missing: str,
        message: str,
    ) -> None:
        inventory_page.add_to_cart(BACKPACK)
        checkout = (
            inventory_page.open_cart().expect_loaded().start_checkout().expect_loaded()
        )

        checkout.fill_details(first, last, postal).continue_button.click()

        assert checkout.error_text == message
        assert "step-two" not in checkout.current_url
