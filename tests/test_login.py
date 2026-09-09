"""Сценарии авторизации."""
from __future__ import annotations

import allure
import pytest

from pages.login_page import LoginPage

LOCKED_OUT_ERROR = "Epic sadface: Sorry, this user has been locked out."
WRONG_CREDENTIALS_ERROR = (
    "Epic sadface: Username and password do not match any user in this service"
)


@allure.epic("SauceDemo")
@allure.feature("Авторизация")
class TestLogin:
    @allure.story("Успешный вход")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Пользователь «{user}» попадает в каталог")
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "user",
        ["standard_user", "problem_user", "visual_user", "error_user"],
    )
    def test_login_succeeds(self, login_page: LoginPage, user: str) -> None:
        inventory = login_page.login(user).expect_loaded()

        assert inventory.items.count() == 6, "В каталоге должно быть 6 товаров"

    @allure.story("Заблокированный пользователь")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Заблокированный пользователь получает понятную ошибку")
    @pytest.mark.smoke
    def test_locked_out_user_rejected(self, login_page: LoginPage) -> None:
        login_page.try_login("locked_out_user", "secret_sauce")

        assert login_page.error_text == LOCKED_OUT_ERROR
        assert "inventory" not in login_page.current_url

    @allure.story("Неверные данные")
    @allure.title("Неверный пароль не пускает в систему")
    @pytest.mark.regression
    def test_wrong_password_rejected(self, login_page: LoginPage) -> None:
        login_page.try_login("standard_user", "wrong_password")

        assert login_page.error_text == WRONG_CREDENTIALS_ERROR

    @allure.story("Валидация формы")
    @allure.title("Пустое поле «{field}» блокирует вход")
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "user, password, field, message",
        [
            ("", "secret_sauce", "логин", "Epic sadface: Username is required"),
            ("standard_user", "", "пароль", "Epic sadface: Password is required"),
        ],
    )
    def test_empty_field_blocks_login(
        self,
        login_page: LoginPage,
        user: str,
        password: str,
        field: str,
        message: str,
    ) -> None:
        login_page.try_login(user, password)

        assert login_page.error_text == message

    @allure.story("Производительность")
    @allure.title("Медленный пользователь всё же доходит до каталога")
    @pytest.mark.regression
    def test_performance_glitch_user_eventually_loads(
        self, login_page: LoginPage
    ) -> None:
        inventory = login_page.login("performance_glitch_user")
        inventory.page.wait_for_url("**/inventory.html", timeout=30_000)

        assert inventory.items.count() == 6
