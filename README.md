# UI-автотесты SauceDemo

Автотесты интернет-магазина [SauceDemo](https://www.saucedemo.com/) на Playwright
по паттерну Page Object: авторизация, каталог, корзина и сквозное оформление заказа.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.49-2EAD33?logo=playwright&logoColor=white)
![Pytest](https://img.shields.io/badge/pytest-8.3-0A9EDC?logo=pytest&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-2.13-FF6B6B)

## Что покрыто

**26 тестов**: 24 проходят, 2 зафиксированы как дефекты стенда.

| Набор | Тестов | Что проверяет |
|---|---|---|
| Авторизация | 9 | вход четырьмя ролями, блокировка, неверный пароль, валидация полей, медленный пользователь |
| Каталог | 7 | состав, счётчик корзины, сортировка по цене и имени, дефекты `problem_user` |
| Корзина | 3 | состав, пустое состояние, возврат в каталог без потери товаров |
| Оформление | 5 | сквозной путь до подтверждения, расчёт налога 8%, обязательные поля |

Найдено и задокументировано **2 дефекта** — см. [docs/BUGS.md](docs/BUGS.md).

## Скорость

| Режим | Время |
|---|---|
| Последовательно | 44 с |
| `pytest -n 4` | **17.7 с** |

## Стек

- **Playwright** — автоожидания вместо `sleep`, headless-прогон в CI
- **Page Object** — локаторы живут в `pages/`, тесты читаются как сценарии
- **pytest** — фикстуры, параметризация, маркеры `smoke` / `regression` / `defect`
- **pytest-xdist** — параллельный прогон в четыре потока
- **Allure** — шаги, а при падении автоматически скриншот, HTML страницы и URL

## Запуск

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
pytest
```

Быстрые варианты:

```bash
pytest -m smoke        # критичный путь
pytest -n 4            # параллельно
pytest --headed        # с открытым браузером, для отладки
```

Отчёт Allure локально (нужен [Allure CLI](https://allurereport.org/docs/install/)):

```bash
allure serve allure-results
```

## Структура

```
├── pages/
│   ├── base_page.py       # открытие страницы, ожидание загрузки, скриншоты
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py   # три шага оформления
├── tests/
│   ├── conftest.py        # фикстуры и хук со скриншотом при падении
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   └── test_checkout.py
├── docs/BUGS.md
└── .github/workflows/tests.yml
```

## Решения, которые стоит пояснить

**Скриншот прикладывается автоматически.** Хук `pytest_runtest_makereport`
ловит падение и кладёт в отчёт снимок экрана, HTML страницы и URL — по упавшему
тесту в CI видно, что произошло, без локального воспроизведения.

**Методы страниц возвращают следующую страницу.** `login()` отдаёт `InventoryPage`,
`start_checkout()` — `CheckoutPage`. Поэтому сценарий пишется цепочкой и читается
как описание пути пользователя.

**Фиксированный вьюпорт 1440×900.** Без него вёрстка различается между локальной
машиной и раннером, и тесты начинают «моргать» на пустом месте.

**Никаких `sleep`.** Playwright ждёт элементы сам; единственный явный таймаут —
30 секунд для `performance_glitch_user`, который тормозит по замыслу стенда.
