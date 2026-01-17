# QA Final Project: Tandoor Meal Plan Testing

Этот проект содержит автоматизированные тесты для smoke-тестирования раздела Meal Plan веб-приложения Tandoor с использованием Python, Selenium WebDriver и requests.

## Описание проекта

Проект автоматизирует тестирование ключевых сценариев управления планами питания в Tandoor:
- Создание, просмотр и удаление планов питания
- Работа со списком покупок
- API-интеграция для подготовки тестовых данных

## Технологии

- Python 3.11
- Selenium WebDriver
- pytest
- requests
- Allure для отчетов
- GitLab CI/CD

## Требования

- Python 3.11+
- Google Chrome
- Git
- Аккаунт в Tandoor
- API-токен от Tandoor

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd qa_auto_tandoor
   ```

2. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Настройте переменные окружения в `.env`:
   ```
   BASE_URL=https://app.tandoor.dev
   TANDOOR_TOKEN=your_token_here
   TANDOOR_USERNAME=your_username_here
   TANDOOR_PASSWORD=your_password_here
   ```

## Получение API-токена

1. Авторизуйтесь в Tandoor
2. Перейдите в раздел API в настройках
3. Создайте новый токен с правами "write"
4. Сохраните токен в `.env`

## Структура проекта

```
qa_auto_tandoor/
├── api/                    # API-клиент
│   └── client.py
├── pages/                  # Page Object Model классы
│   ├── base_page.py
│   ├── header_component.py
│   ├── login_page.py
│   ├── meal_plan_page.py
│   └── shopping_list_page.py
├── tests/                  # Тесты
│   ├── test_api_client.py
│   └── test_ui_meal_plan.py
├── conftest.py             # Фикстуры и хуки pytest
├── generate_test_data.py   # Генерация тестовых данных
├── test_data.json          # Ссылки на рецепты
├── requirements.txt        # Зависимости
├── pytest.ini             # Конфигурация pytest
├── .env                   # Переменные окружения
├── .gitignore
└── .gitlab-ci.yml         # CI/CD конфигурация
```

## Реализованные сценарии тестирования

### API-тесты
- Получение списка рецептов
- Создание плана питания
- Удаление плана питания
- Получение списка покупок

### UI-тесты
- Авторизация в приложении
- Создание плана питания
- Просмотр плана питания
- Удаление плана питания
- Проверка списка покупок

## Запуск тестов

### Запуск всех тестов
```bash
pytest
```

### Запуск API-тестов
```bash
pytest -m api
```

### Запуск UI-тестов
```bash
pytest -m ui
```

### Генерация Allure-отчета
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## CI/CD

Проект настроен для автоматического запуска тестов в GitLab CI с генерацией Allure-отчетов и публикацией на GitLab Pages.

## Особенности

- Тесты используют headless-режим браузера для ускорения
- API-клиент обрабатывает ошибки и предоставляет понятные сообщения
- Page Object Model обеспечивает поддерживаемость UI-тестов
- Автоматическая генерация скриншотов при падении UI-тестов
