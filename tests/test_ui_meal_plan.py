import pytest
import allure
import os
from pages.login_page import LoginPage
from pages.header_component import HeaderComponent
from pages.meal_plan_page import MealPlanPage
from pages.shopping_list_page import ShoppingListPage
from generate_test_data import generate_test_data

@pytest.mark.ui
@allure.feature("Meal Plan UI")
@allure.story("Test Meal Plan creation and management")
class TestMealPlanUI:
    def setup_method(self):
        self.base_url = os.getenv('BASE_URL')

    @allure.step("Login to Tandoor")
    def login(self, driver):
        login_page = LoginPage(driver)
        login_page.open_url(f"{self.base_url}/accounts/login/")
        login_page.login(os.getenv('TANDOOR_USERNAME'), os.getenv('TANDOOR_PASSWORD'))

    @allure.step("Create meal plan")
    def test_create_meal_plan(self, driver, get_or_create_recipe):
        self.login(driver)
        header = HeaderComponent(driver)
        header.go_to_meal_plan()

        meal_plan = MealPlanPage(driver)
        data = generate_test_data()
        meal_plan.create_plan(
            title=data['title'],
            from_date=data['from_date'],
            to_date=data['to_date'],
            meal_type=data['meal_type'],
            recipe=str(get_or_create_recipe),
            servings=data['servings'],
            add_to_list=True
        )
        assert meal_plan.is_plan_created(data['title'])

    @allure.step("View meal plan")
    def test_view_meal_plan(self, driver, get_or_create_recipe):
        self.login(driver)
        header = HeaderComponent(driver)
        header.go_to_meal_plan()
        
        # Сначала создаем план для просмотра
        meal_plan = MealPlanPage(driver)
        data = generate_test_data()
        meal_plan.create_plan(
            title=data['title'],
            from_date=data['from_date'],
            to_date=data['to_date'],
            meal_type=data['meal_type'],
            recipe=str(get_or_create_recipe),
            servings=data['servings'],
            add_to_list=False
        )
        
        # Проверяем, что план виден
        assert meal_plan.is_element_visible(MealPlanPage.PLAN_ITEM)

    @allure.step("Delete meal plan")
    def test_delete_meal_plan(self, driver, get_or_create_recipe, api_client):
        self.login(driver)
        header = HeaderComponent(driver)
        header.go_to_meal_plan()
        meal_plan = MealPlanPage(driver)
        
        # Сначала создаем план для удаления
        data = generate_test_data()
        meal_plan.create_plan(
            title=data['title'],
            from_date=data['from_date'],
            to_date=data['to_date'],
            meal_type=data['meal_type'],
            recipe=str(get_or_create_recipe),
            servings=data['servings'],
            add_to_list=False
        )
        
        # Удаляем план через UI
        meal_plan.delete_plan(data['title'])
        assert not meal_plan.is_plan_created(data['title'])
        
        # Кросс-проверка через API: убеждаемся, что план действительно удален из базы
        # Ищем план по названию
        plans = api_client.get_meal_plans()
        if plans and 'results' in plans:
            for plan in plans['results']:
                if plan['title'] == data['title']:
                    pytest.fail(f"Meal plan '{data['title']}' still exists in database after UI deletion")

    @allure.step("Check shopping list")
    def test_check_shopping_list(self, driver, get_or_create_recipe):
        self.login(driver)
        header = HeaderComponent(driver)
        header.go_to_meal_plan()
        
        # Сначала создаем план с добавлением в список покупок
        meal_plan = MealPlanPage(driver)
        data = generate_test_data()
        meal_plan.create_plan(
            title=data['title'],
            from_date=data['from_date'],
            to_date=data['to_date'],
            meal_type=data['meal_type'],
            recipe=str(get_or_create_recipe),
            servings=data['servings'],
            add_to_list=True
        )
        
        # Проверяем список покупок
        header.go_to_shopping_list()
        shopping_list = ShoppingListPage(driver)
        initial_count = shopping_list.get_items_count()
        assert initial_count > 0
        shopping_list.mark_item_as_bought()
        assert shopping_list.is_item_checked()
