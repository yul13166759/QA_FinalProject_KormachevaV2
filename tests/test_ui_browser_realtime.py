import pytest
import allure
import time
import os
from pages.login_page import LoginPage
from pages.header_component import HeaderComponent
from pages.meal_plan_page import MealPlanPage
from pages.shopping_list_page import ShoppingListPage
from generate_test_data import generate_test_data

@pytest.mark.ui
@pytest.mark.browser
@allure.feature("Meal Plan UI - Real Browser")
@allure.story("Test Meal Plan creation and management with real browser")
class TestMealPlanUIBrowser:
    """Тесты с реальным браузером (без headless режима)"""
    
    def setup_method(self):
        self.base_url = os.getenv('BASE_URL', 'https://app.tandoor.dev')

    @allure.step("Login to Tandoor")
    def login(self, driver):
        login_page = LoginPage(driver)
        login_page.open_url(f"{self.base_url}/accounts/login/")
        login_page.login(os.getenv('TANDOOR_USERNAME'), os.getenv('TANDOOR_PASSWORD'))

    @allure.step("Create meal plan")
    def test_create_meal_plan_browser(self, logged_in_browser, get_or_create_recipe):
        """Создание плана питания с отображением в реальном браузере"""
        header = HeaderComponent(logged_in_browser)
        header.go_to_meal_plan()

        # Пауза для визуализации
        time.sleep(2)

        meal_plan = MealPlanPage(logged_in_browser)
        data = generate_test_data()
        
        print(f"\nСоздаём план: {data['title']}")
        
        meal_plan.create_plan(
            title=data['title'],
            from_date=data['from_date'],
            to_date=data['to_date'],
            meal_type=data['meal_type'],
            recipe=str(get_or_create_recipe),
            servings=data['servings'],
            add_to_list=True
        )
        
        # Пауза для визуализации результата
        time.sleep(3)
        
        assert meal_plan.is_plan_created(data['title'])
        print(f"✓ План '{data['title']}' успешно создан!")

    @allure.step("View meal plan")
    def test_view_meal_plan_browser(self, logged_in_browser, get_or_create_recipe):
        """Просмотр плана питания с отображением в реальном браузере"""
        header = HeaderComponent(logged_in_browser)
        header.go_to_meal_plan()
        
        time.sleep(2)
        
        # Создаем план для просмотра
        meal_plan = MealPlanPage(logged_in_browser)
        data = generate_test_data()
        
        print(f"\nСоздаём план для просмотра: {data['title']}")
        
        meal_plan.create_plan(
            title=data['title'],
            from_date=data['from_date'],
            to_date=data['to_date'],
            meal_type=data['meal_type'],
            recipe=str(get_or_create_recipe),
            servings=data['servings'],
            add_to_list=False
        )
        
        time.sleep(3)
        
        # Проверяем, что план виден
        assert meal_plan.is_element_visible(MealPlanPage.PLAN_ITEM)
        print(f"✓ План '{data['title']}' отображается на странице!")

    @allure.step("Delete meal plan")
    def test_delete_meal_plan_browser(self, logged_in_browser, get_or_create_recipe, api_client):
        """Удаление плана питания с отображением в реальном браузере"""
        header = HeaderComponent(logged_in_browser)
        header.go_to_meal_plan()
        
        time.sleep(2)
        
        meal_plan = MealPlanPage(logged_in_browser)
        
        # Создаем план для удаления
        data = generate_test_data()
        
        print(f"\nСоздаём план для удаления: {data['title']}")
        
        meal_plan.create_plan(
            title=data['title'],
            from_date=data['from_date'],
            to_date=data['to_date'],
            meal_type=data['meal_type'],
            recipe=str(get_or_create_recipe),
            servings=data['servings'],
            add_to_list=False
        )
        
        time.sleep(2)
        
        # Удаляем план через UI
        print(f"Удаляем план: {data['title']}")
        meal_plan.delete_plan(data['title'])
        
        time.sleep(2)
        
        assert not meal_plan.is_plan_created(data['title'])
        
        # Кросс-проверка через API
        plans = api_client.get_meal_plans()
        if plans and 'results' in plans:
            for plan in plans['results']:
                if plan['title'] == data['title']:
                    pytest.fail(f"Meal plan '{data['title']}' still exists in database after UI deletion")
        
        print(f"✓ План '{data['title']}' успешно удалён!")

    @allure.step("Check shopping list")
    def test_check_shopping_list_browser(self, logged_in_browser, get_or_create_recipe):
        """Проверка списка покупок с отображением в реальном браузере"""
        header = HeaderComponent(logged_in_browser)
        header.go_to_meal_plan()
        
        time.sleep(2)
        
        # Создаем план с добавлением в список покупок
        meal_plan = MealPlanPage(logged_in_browser)
        data = generate_test_data()
        
        print(f"\nСоздаём план со списком покупок: {data['title']}")
        
        meal_plan.create_plan(
            title=data['title'],
            from_date=data['from_date'],
            to_date=data['to_date'],
            meal_type=data['meal_type'],
            recipe=str(get_or_create_recipe),
            servings=data['servings'],
            add_to_list=True
        )
        
        time.sleep(2)
        
        # Проверяем список покупок
        header.go_to_shopping_list()
        
        time.sleep(2)
        
        shopping_list = ShoppingListPage(logged_in_browser)
        initial_count = shopping_list.get_items_count()
        
        print(f"Найдено элементов в списке покупок: {initial_count}")
        
        assert initial_count > 0, "Список покупок пуст!"
        
        shopping_list.mark_item_as_bought()
        
        time.sleep(2)
        
        assert shopping_list.is_item_checked()
        print("✓ Элемент отмечен как купленный!")
