import pytest
import allure
from generate_test_data import generate_test_data

@pytest.mark.api
@allure.feature("API Client")
@allure.story("Test API Client functionality")
class TestAPIClient:
    @allure.step("Get list of recipes")
    def test_get_recipes(self, api_client):
        recipes = api_client.get_recipes()
        assert recipes is not None
        assert 'results' in recipes

    @allure.step("Create meal plan")
    def test_create_meal_plan(self, api_client, get_or_create_recipe):
        data = generate_test_data()
        if get_or_create_recipe:
            data['recipe'] = get_or_create_recipe
            plan = api_client.create_meal_plan(data)
            assert plan is not None
            assert 'id' in plan

    @allure.step("Delete meal plan")
    def test_delete_meal_plan(self, api_client, get_or_create_recipe):
        # Создать план для удаления
        data = generate_test_data()
        data['recipe'] = get_or_create_recipe
        plan = api_client.create_meal_plan(data)
        assert plan is not None
        assert 'id' in plan
        plan_id = plan['id']

        # Удалить план
        result = api_client.delete_meal_plan(plan_id)
        assert result is True

        # Проверить, что план действительно удален
        deleted_plan = api_client.get_meal_plan(plan_id)
        assert deleted_plan is None

    @allure.step("Get shopping list")
    def test_get_shopping_list(self, api_client):
        shopping_list = api_client.get_shopping_list()
        assert shopping_list is not None

    @allure.step("Import recipe")
    def test_import_recipe(self, api_client):
        url = "https://eda.ru/recepty/zavtraki/omlet-s-syrom-i-zelenyu-12345"
        recipe = api_client.import_recipe(url)
        assert recipe is not None
        assert 'id' in recipe

    @allure.step("Delete recipe")
    def test_delete_recipe(self, api_client, get_or_create_recipe):
        if get_or_create_recipe:
            result = api_client.delete_recipe(get_or_create_recipe)
            assert result is True

    @allure.step("Test error handling - delete non-existent meal plan")
    def test_delete_nonexistent_meal_plan(self, api_client):
        result = api_client.delete_meal_plan(99999)  # Несуществующий ID
        assert result is False  # Должно вернуть False при ошибке
