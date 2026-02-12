import pytest
import json
import os
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from api.client import TandoorAPIClient

load_dotenv()

@pytest.fixture
def api_client():
    """Фикстура для API клиента - всегда возвращает клиент, тесты выполняются реально"""
    client = TandoorAPIClient()
    return client

@pytest.fixture
def load_test_data():
    with open('test_data.json', 'r') as f:
        return json.load(f)

@pytest.fixture
def get_or_create_recipe(api_client):
    recipes = api_client.get_recipes()
    if recipes and 'results' in recipes and recipes['results']:
        return recipes['results'][0]['id']
    else:
        # Импортировать рецепт
        url = "https://eda.ru/recepty/zavtraki/omlet-s-syrom-i-zelenyu-12345"  # Пример
        recipe = api_client.import_recipe(url)
        return recipe['id'] if recipe else None

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    if os.getenv('CI'):
        # В CI используем Selenium Grid
        try:
            driver = webdriver.Remote(
                command_executor='http://selenium:4444/wd/hub',
                options=options
            )
        except Exception as e:
            pytest.skip(f"Selenium недоступен: {e}")
    else:
        # Локально
        try:
            driver = webdriver.Chrome(options=options)
        except Exception as e:
            pytest.skip(f"Chrome недоступен: {e}")
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def browser_driver():
    """Фикстура для запуска тестов с реальным браузером (без headless)"""
    from selenium import webdriver
    
    options = Options()
    # Убираем headless режим для реального отображения браузера
    # options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1920, 1080)
        # Увеличиваем таймауты
        driver.set_page_load_timeout(120)
        driver.implicitly_wait(20)
    except Exception as e:
        pytest.skip(f"Chrome недоступен: {e}")
    
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def logged_in_browser(browser_driver):
    """Фикстура для входа в систему с реальным браузером"""
    from pages.login_page import LoginPage
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    import os
    import time
    
    login_page = LoginPage(browser_driver)
    base_url = os.getenv('BASE_URL', 'https://app.tandoor.dev')
    
    print(f"\n🌐 Открываем страницу логина: {base_url}/accounts/login/")
    
    # Открываем страницу логина с увеличенным таймаутом
    browser_driver.get(f"{base_url}/accounts/login/")
    
    # Ждем загрузки страницы - проверяем URL
    for i in range(30):  # 30 секунд максимум
        current_url = browser_driver.current_url
        print(f"   Попытка {i+1}: URL = {current_url}")
        if 'tandoor.dev' in current_url or 'app.tandoor' in current_url:
            break
        time.sleep(1)
    
    # Ждем появления body
    print("   Ожидаем загрузку body...")
    WebDriverWait(browser_driver, 60).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    
    # Ждем появления формы логина (поле username)
    print("   Ожидаем форму логина...")
    WebDriverWait(browser_driver, 60).until(
        EC.presence_of_element_located((By.NAME, 'login'))
    )
    
    print("   ✅ Страница загружена, выполняем логин...")
    
    # Выполняем логин
    login_page.login(os.getenv('TANDOOR_USERNAME'), os.getenv('TANDOOR_PASSWORD'))
    
    # Ждем завершения логина
    time.sleep(3)
    
    yield browser_driver

@pytest.fixture(scope="module")
def logged_in_driver(driver):
    """Фикстура для входа в систему один раз на модуль"""
    from pages.login_page import LoginPage
    import os
    
    base_url = os.getenv('BASE_URL')
    
    # ЗАЩИТА: проверяем, что BASE_URL задан правильно
    if not base_url or base_url == '$BASE_URL' or '://' not in str(base_url):
        pytest.skip(f"BASE_URL не настроен правильно: {base_url}. Пропускаем тест.")
    
    login_page = LoginPage(driver)
    login_page.open_url(f"{base_url}/accounts/login/")
    login_page.login(os.getenv('TANDOOR_USERNAME'), os.getenv('TANDOOR_PASSWORD'))
    yield driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver')
        if driver:
            try:
                # Проверяем, что сессия ещё активна
                driver.current_url
                screenshot = driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Screenshot", attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                print(f"Could not capture screenshot: {e}")
