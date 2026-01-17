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
            # Сохранить ID для удаления
            pytest.plan_id = plan['id']

    @allure.step("Delete meal plan")
    def test_delete_meal_plan(self, api_client):
        if hasattr(pytest, 'plan_id'):
            result = api_client.delete_meal_plan(pytest.plan_id)
            assert result is True

    @allure.step("Get shopping list")
    def test_get_shopping_list(self, api_client):
        shopping_list = api_client.get_shopping_list()
        assert shopping_list is not None
