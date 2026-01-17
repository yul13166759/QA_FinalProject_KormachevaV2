import requests
from dotenv import load_dotenv
import os

load_dotenv()

class TandoorAPIClient:
    def __init__(self):
        self.base_url = os.getenv('BASE_URL')
        self.token = os.getenv('TANDOOR_TOKEN')
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, method, endpoint, data=None, params=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, json=data, params=params)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def import_recipe(self, url):
        data = {"url": url}
        response = self._make_request('POST', '/api/bookmarklet/import/', data)
        if response:
            return response.json()
        return None

    def get_recipes(self):
        response = self._make_request('GET', '/api/recipe/')
        if response:
            return response.json()
        return None

    def delete_recipe(self, recipe_id):
        response = self._make_request('DELETE', f'/api/recipe/{recipe_id}/')
        return response is not None

    def create_meal_plan(self, data):
        response = self._make_request('POST', '/api/plan/', data)
        if response:
            return response.json()
        return None

    def get_meal_plan(self, plan_id):
        response = self._make_request('GET', f'/api/plan/{plan_id}/')
        if response:
            return response.json()
        return None

    def delete_meal_plan(self, plan_id):
        response = self._make_request('DELETE', f'/api/plan/{plan_id}/')
        return response is not None

    def get_shopping_list(self):
        response = self._make_request('GET', '/api/shopping-list/')
        if response:
            return response.json()
        return None

    def test_connection(self):
        recipes = self.get_recipes()
        if recipes:
            print("Connection successful. Recipes:", recipes)
        else:
            print("Connection failed.")

if __name__ == "__main__":
    client = TandoorAPIClient()
    client.test_connection()
