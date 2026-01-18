# Архитектура проекта QA_FinalProject_KormachevaV2

## Обзор
Это автоматизированный QA проект для тестирования веб-приложения. Проект использует Python с pytest для выполнения тестов, Selenium для UI тестирования и Allure для отчетности.

## Структура проекта

```
QA_FinalProject_KormachevaV2/
├── .gitlab-ci.yml          # Конфигурация GitLab CI/CD
├── .gitignore              # Игнорируемые файлы для Git
├── conftest.py             # Конфигурация pytest
├── generate_test_data.py   # Скрипт генерации тестовых данных
├── pytest.ini              # Конфигурация pytest
├── README.md               # Документация проекта
├── requirements.txt        # Зависимости Python
├── test_data.json          # Тестовые данные
├── api/
│   └── client.py           # API клиент для взаимодействия с сервером
├── pages/
│   ├── base_page.py        # Базовый класс для страниц
│   ├── header_component.py # Компонент заголовка
│   ├── login_page.py       # Страница входа
│   ├── meal_plan_page.py   # Страница плана питания
│   └── shopping_list_page.py # Страница списка покупок
└── tests/
    ├── test_api_client.py  # Тесты API
    └── test_ui_meal_plan.py # UI тесты плана питания
```

## Компоненты

### API слой
- **client.py**: Реализует HTTP запросы к API сервера. Используется для тестирования backend функциональности.

### UI слой
- **base_page.py**: Базовый класс для всех страниц, содержит общие методы для работы с элементами страницы.
- **header_component.py**: Класс для работы с компонентом заголовка сайта.
- **login_page.py**: Класс для страницы авторизации.
- **meal_plan_page.py**: Класс для страницы управления планом питания.
- **shopping_list_page.py**: Класс для страницы списка покупок.

### Тесты
- **test_api_client.py**: Тесты API эндпоинтов с использованием pytest и маркировки.
- **test_ui_meal_plan.py**: UI тесты с использованием Selenium WebDriver.

## CI/CD Pipeline
GitLab CI состоит из трех стадий:
1. **prepare**: Подготовка окружения, установка зависимостей
2. **test**: Запуск API и UI тестов с генерацией Allure отчетов
3. **report**: Генерация и публикация отчетов о тестировании

## Технологии
- **Python 3.11**: Основной язык программирования
- **pytest**: Фреймворк для тестирования
- **Selenium**: Для автоматизации браузера
- **Allure**: Для генерации отчетов
- **GitLab CI/CD**: Для непрерывной интеграции и доставки

## Зависимости
Список зависимостей находится в `requirements.txt`. Основные пакеты:
- pytest
- selenium
- requests
- allure-pytest

## Запуск тестов локально
1. Установить зависимости: `pip install -r requirements.txt`
2. Запустить API тесты: `pytest tests/test_api_client.py -m api`
3. Запустить UI тесты: `pytest tests/test_ui_meal_plan.py -m ui`
4. Сгенерировать отчет: `allure generate allure-results -o allure-report`
