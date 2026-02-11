import requests
from dotenv import load_dotenv
import os
from requests.auth import HTTPBasicAuth

load_dotenv()

class TandoorAPIClient:
    def __init__(self):
        self.base_url = os.getenv('BASE_URL')
        self.token = os.getenv('TANDOOR_TOKEN')
        self.username = os.getenv('TANDOOR_USERNAME')
        self.password = os.getenv('TANDOOR_PASSWORD')
        
        # Создаем сессию для сохранения cookies
        self.session = requests.Session()
        
        # Используем базовую авторизацию + токен в заголовке
        self.headers = {
            'Content-Type': 'application/json'
        }
        
        # Добавляем токен если есть (формат для Tandoor)
        if self.token:
            self.headers['Authorization'] = f'Token {self.token}'
        
        # Базовая авторизация для API
        self.auth = HTTPBasicAuth(self.username, self.password) if self.username and self.password else None
        
        # Пробуем залогиниться для получения сессии
        self._login()
    
    def _login(self):
        """Вход в систему для получения сессионных кук"""
        try:
            # Сначала получаем CSRF токен
            login_page = self.session.get(f"{self.base_url}/accounts/login/")
            if login_page.status_code == 200:
                # Извлекаем CSRF токен из HTML
                import re
                csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', login_page.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    
                    # Логинимся
                    login_data = {
                        'csrfmiddlewaretoken': csrf_token,
                        'login': self.username,
                        'password': self.password,
                    }
                    login_headers = {
                        'Referer': f"{self.base_url}/accounts/login/",
                        'X-CSRFToken': csrf_token
                    }
                    login_response = self.session.post(
                        f"{self.base_url}/accounts/login/",
                        data=login_data,
                        headers=login_headers
                    )
                    if login_response.status_code == 200 or login_response.status_code == 302:
                        print("Session login successful")
                    else:
                        print(f"Session login failed: {login_response.status_code}")
        except Exception as e:
            print(f"Session login error: {e}")

    def _make_request(self, method, endpoint, data=None, params=None):
        url = f"{self.base_url}{endpoint}"
        try:
            # Используем сессию для сохранения cookies
            response = self.session.request(
                method, 
                url, 
                headers=self.headers, 
                json=data, 
                params=params,
                auth=self.auth,
                timeout=30
            )
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                print(f"Error 403 Forbidden: {e} - Недостаточно прав доступа")
            else:
                print(f"HTTP Error: {e}")
            return None
        except requests.exceptions.Timeout:
            print(f"Error: Request timeout for {url}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def import_recipe(self, url):
        data = {"url": url}
        response = self._make_request('POST', '/api/bookmarklet/import/', data)
        if response:
            return self._safe_json_parse(response)
        return None

    def get_recipes(self):
        response = self._make_request('GET', '/api/recipe/')
        if response:
            return self._safe_json_parse(response)
        return None

    def get_recipe(self, recipe_id):
        """Получить рецепт по ID"""
        response = self._make_request('GET', f'/api/recipe/{recipe_id}/')
        if response:
            return self._safe_json_parse(response)
        return None

    def delete_recipe(self, recipe_id):
        response = self._make_request('DELETE', f'/api/recipe/{recipe_id}/')
        return response is not None

    def create_meal_plan(self, data):
        response = self._make_request('POST', '/api/plan/', data)
        if response:
            return self._safe_json_parse(response)
        return None

    def get_meal_plan(self, plan_id):
        response = self._make_request('GET', f'/api/plan/{plan_id}/')
        if response:
            return self._safe_json_parse(response)
        return None

    def delete_meal_plan(self, plan_id):
        response = self._make_request('DELETE', f'/api/plan/{plan_id}/')
        return response is not None

    def get_shopping_list(self):
        response = self._make_request('GET', '/api/shopping-list/')
        if response:
            return self._safe_json_parse(response)
        return None

    def _safe_json_parse(self, response):
        """Безопасный парсинг JSON с проверкой content-type"""
        content_type = response.headers.get('content-type', '')
        if 'application/json' in content_type:
            try:
                return response.json()
            except ValueError:
                print(f"Error: Invalid JSON response from {response.url}")
                return None
        else:
            print(f"Error: Expected JSON but got {content_type} from {response.url}")
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
