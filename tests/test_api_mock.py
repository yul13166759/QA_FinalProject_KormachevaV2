import pytest
import allure
import requests
from datetime import datetime, timedelta

# Мок-сервер на localhost:8000
BASE_URL = "http://localhost:8000"

@pytest.fixture
def mock_api_client():
    """Клиент для мок-сервера"""
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'Authorization': 'Token mock_token'
    })
    return session

@allure.feature("API Tests with Mock Server")
@allure.story("Recipes")
@pytest.mark.api
@pytest.mark.mock
class TestAPIMock:
    
    @allure.step("Get recipes from mock server")
    def test_get_recipes_mock(self, mock_api_client):
        """Получение списка рецептов"""
        response = mock_api_client.get(f"{BASE_URL}/api/recipe/")
        assert response.status_code == 200
        data = response.json()
        assert 'results' in data
        assert len(data['results']) > 0
        allure.attach(str(data), name="Recipes", attachment_type=allure.attachment_type.TEXT)
    
    @allure.step("Create meal plan on mock server")
    def test_create_meal_plan_mock(self, mock_api_client):
        """Создание плана питания"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        data = {
            'recipe': 1,
            'title': 'Test Plan Mock',
            'meal_type': 'Dinner',
            'date': tomorrow,
            'servings': 2,
            'note': 'Test note'
        }
        response = mock_api_client.post(f"{BASE_URL}/api/plan/", json=data)
        assert response.status_code == 201
        result = response.json()
        assert result['title'] == 'Test Plan Mock'
        allure.attach(str(result), name="Created Plan", attachment_type=allure.attachment_type.TEXT)
    
    @allure.step("Get shopping list from mock server")
    def test_get_shopping_list_mock(self, mock_api_client):
        """Получение списка покупок"""
        response = mock_api_client.get(f"{BASE_URL}/api/shopping-list/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        allure.attach(str(data), name="Shopping List", attachment_type=allure.attachment_type.TEXT)
    
    @allure.step("Delete meal plan on mock server")
    def test_delete_meal_plan_mock(self, mock_api_client):
        """Удаление плана питания"""
        # Сначала создадим план
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        data = {
            'recipe': 1,
            'title': 'Plan to Delete',
            'meal_type': 'Lunch',
            'date': tomorrow,
            'servings': 1
        }
        create_response = mock_api_client.post(f"{BASE_URL}/api/plan/", json=data)
        assert create_response.status_code == 201
        plan_id = create_response.json()['id']
        
        # Удаляем план
        delete_response = mock_api_client.delete(f"{BASE_URL}/api/plan/{plan_id}/")
        assert delete_response.status_code == 204
        allure.attach(f"Deleted plan ID: {plan_id}", name="Deleted Plan", attachment_type=allure.attachment_type.TEXT)
