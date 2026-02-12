import pytest
import allure
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.ui
@pytest.mark.local
@allure.feature("Meal Plan UI - Local Mock Server")
@allure.story("Test with local mock Tandoor server")
class TestMealPlanUILocal:
    """Тесты с локальным мок-сервером (упрощённые локаторы)"""
    
    def setup_method(self):
        self.base_url = os.getenv('BASE_URL', 'http://localhost:8000')

    @allure.step("Login to local Tandoor")
    def test_login_local(self, browser_driver):
        """Тест логина на локальном сервере"""
        login_url = f"{self.base_url}/accounts/login/"
        print(f"\n🌐 Открываем {login_url}")
        
        browser_driver.get(login_url)
        
        # Ждем загрузки формы
        WebDriverWait(browser_driver, 10).until(
            EC.presence_of_element_located((By.NAME, "login"))
        )
        
        print("   ✅ Форма логина загружена")
        
        # Заполняем поля
        browser_driver.find_element(By.NAME, "login").send_keys("admin")
        browser_driver.find_element(By.NAME, "password").send_keys("admin")
        
        print("   📝 Вводим логин/пароль")
        
        # Кликаем по кнопке
        browser_driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Ждем перехода
        WebDriverWait(browser_driver, 10).until(
            EC.url_contains("/plan/")
        )
        
        print(f"   ✅ Успешный логин! URL: {browser_driver.current_url}")
        
        # Пауза для визуализации
        time.sleep(3)
        
        assert "/plan/" in browser_driver.current_url

    @allure.step("Create meal plan on local server")
    def test_create_meal_plan_local(self, browser_driver):
        """Создание плана питания на локальном сервере"""
        # Сначала логинимся
        self._do_login(browser_driver)
        
        print("\n📋 Создаём план питания...")
        
        # Ждем загрузки страницы
        WebDriverWait(browser_driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        
        # Заполняем форму создания плана
        from datetime import datetime, timedelta
        
        title = f"Test Plan {datetime.now().strftime('%H%M%S')}"
        from_date = datetime.now().strftime('%Y-%m-%d')
        to_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        browser_driver.find_element(By.NAME, "title").send_keys(title)
        browser_driver.find_element(By.NAME, "from_date").send_keys(from_date)
        browser_driver.find_element(By.NAME, "to_date").send_keys(to_date)
        
        print(f"   📝 Заполнили: {title}")
        
        # Выбираем рецепт
        recipe_select = browser_driver.find_element(By.NAME, "recipe")
        recipe_select.click()
        
        # Кликаем по кнопке создания
        browser_driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        print("   ✅ План создан!")
        
        # Пауза для визуализации
        time.sleep(3)
        
        # Проверяем, что план появился на странице
        assert title in browser_driver.page_source
        print(f"   ✓ План '{title}' найден на странице!")

    @allure.step("View shopping list on local server")
    def test_shopping_list_local(self, browser_driver):
        """Проверка списка покупок"""
        # Логин
        self._do_login(browser_driver)
        
        print("\n🛒 Переходим в список покупок...")
        
        # Кликаем по ссылке Shopping List
        shopping_link = browser_driver.find_element(By.CSS_SELECTOR, "a[href*='shopping']")
        shopping_link.click()
        
        # Ждем загрузки
        WebDriverWait(browser_driver, 10).until(
            EC.url_contains("/shopping/")
        )
        
        print(f"   ✅ Страница загружена: {browser_driver.current_url}")
        
        # Пауза для визуализации
        time.sleep(3)
        
        assert "/shopping/" in browser_driver.current_url

    def _do_login(self, driver):
        """Вспомогательный метод для логина"""
        login_url = f"{self.base_url}/accounts/login/"
        driver.get(login_url)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "login"))
        )
        
        driver.find_element(By.NAME, "login").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        WebDriverWait(driver, 10).until(
            EC.url_contains("/plan/")
        )
